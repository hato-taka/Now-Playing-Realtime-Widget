import React from 'react';
import styled from 'styled-components';

const Button = styled.button`
  background: linear-gradient(45deg, #1db954, #1ed760);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(29, 185, 84, 0.4);
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const SpotifyIcon = styled.span`
  font-size: 24px;
`;

const LoginButton = ({ onClick, disabled = false }) => {
  return (
    <Button onClick={onClick} disabled={disabled}>
      <SpotifyIcon>🎵</SpotifyIcon>
      Spotifyでログイン
    </Button>
  );
};

export default LoginButton; 