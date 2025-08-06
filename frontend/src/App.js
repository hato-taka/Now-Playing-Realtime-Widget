import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import NowPlaying from './components/NowPlaying';
import LoginButton from './components/LoginButton';

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 40px;
`;

const Title = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  color: white;
  margin-bottom: 10px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 20px;
`;

const MainCard = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-width: 600px;
  width: 100%;
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 10px;
  background: ${props => props.isConnected ? 'rgba(29, 185, 84, 0.1)' : 'rgba(231, 76, 60, 0.1)'};
  color: ${props => props.isConnected ? '#1db954' : '#e74c3c'};
  font-weight: 600;
`;

const PulseDot = styled.div`
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: ${props => props.isConnected ? '#1db954' : '#e74c3c'};
  margin-right: 8px;
  animation: ${props => props.isConnected ? 'pulse 2s infinite' : 'none'};
  
  @keyframes pulse {
    0% {
      transform: scale(0.95);
      box-shadow: 0 0 0 0 rgba(29, 185, 84, 0.7);
    }
    
    70% {
      transform: scale(1);
      box-shadow: 0 0 0 10px rgba(29, 185, 84, 0);
    }
    
    100% {
      transform: scale(0.95);
      box-shadow: 0 0 0 0 rgba(29, 185, 84, 0);
    }
  }
`;

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // 認証状態をチェック
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('/current-track');
      if (response.ok) {
        setIsAuthenticated(true);
        // WebSocket接続を開始
        connectWebSocket();
      } else {
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.log('認証されていません');
      setIsAuthenticated(false);
    }
  };

  const connectWebSocket = () => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      console.log('WebSocket接続が確立されました');
      setIsConnected(true);
      setError(null);
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setCurrentTrack(data);
      } catch (error) {
        console.error('WebSocketメッセージの解析エラー:', error);
      }
    };
    
    ws.onclose = () => {
      console.log('WebSocket接続が閉じられました');
      setIsConnected(false);
      // 再接続を試行
      setTimeout(() => {
        if (isAuthenticated) {
          connectWebSocket();
        }
      }, 5000);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocketエラー:', error);
      setError('WebSocket接続エラーが発生しました');
      setIsConnected(false);
    };
  };

  const handleLogin = async () => {
    try {
      const response = await fetch('/auth');
      const data = await response.json();
      
      if (data.auth_url) {
        window.location.href = data.auth_url;
      }
    } catch (error) {
      setError('認証URLの取得に失敗しました');
    }
  };

  return (
    <AppContainer>
      <Header>
        <Title>🎵 Spotify Now Playing</Title>
        <Subtitle>リアルタイムで再生中の曲を共有</Subtitle>
      </Header>

      <MainCard>
        {isAuthenticated && (
          <StatusIndicator isConnected={isConnected}>
            <PulseDot isConnected={isConnected} />
            {isConnected ? 'リアルタイム接続中' : '接続中...'}
          </StatusIndicator>
        )}

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {!isAuthenticated ? (
          <div style={{ textAlign: 'center' }}>
            <h2 style={{ marginBottom: '20px', color: '#333' }}>
              Spotifyにログインしてください
            </h2>
            <p style={{ marginBottom: '30px', color: '#666' }}>
              現在再生中の曲の情報を取得するには、Spotifyアカウントでの認証が必要です。
            </p>
            <LoginButton onClick={handleLogin} />
          </div>
        ) : (
          <NowPlaying track={currentTrack} />
        )}
      </MainCard>
    </AppContainer>
  );
}

export default App; 