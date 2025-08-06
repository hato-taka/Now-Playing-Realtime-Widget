import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  text-align: center;
`;

const LoadingMessage = styled.div`
  font-size: 18px;
  color: #666;
  padding: 40px 0;
`;

const NoTrackMessage = styled.div`
  font-size: 18px;
  color: #666;
  padding: 40px 0;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 15px;
  margin: 20px 0;
`;

const TrackContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
`;

const AlbumArt = styled.div`
  width: 200px;
  height: 200px;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  position: relative;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
`;

const TrackInfo = styled.div`
  text-align: center;
  max-width: 400px;
`;

const TrackName = styled.h2`
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.3;
`;

const ArtistName = styled.h3`
  font-size: 18px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
`;

const AlbumName = styled.p`
  font-size: 14px;
  color: #888;
  margin-bottom: 20px;
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 6px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin: 15px 0;
`;

const ProgressFill = styled.div`
  height: 100%;
  background: linear-gradient(45deg, #1db954, #1ed760);
  border-radius: 3px;
  transition: width 0.3s ease;
  width: ${props => props.progress}%;
`;

const TimeInfo = styled.div`
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #888;
  margin-top: 5px;
`;

const ArtistImages = styled.div`
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 15px;
  flex-wrap: wrap;
`;

const ArtistImage = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  
  img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #1db954;
  }
  
  span {
    font-size: 12px;
    color: #666;
    text-align: center;
    max-width: 60px;
  }
`;

const SpotifyLink = styled.a`
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background: linear-gradient(45deg, #1db954, #1ed760);
  color: white;
  text-decoration: none;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(29, 185, 84, 0.3);
  }
`;

const formatTime = (ms) => {
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

const NowPlaying = ({ track }) => {
  if (!track) {
    return (
      <Container>
        <LoadingMessage>曲の情報を取得中...</LoadingMessage>
      </Container>
    );
  }

  if (!track.is_playing) {
    return (
      <Container>
        <NoTrackMessage>
          {track.message || '現在再生中の曲はありません'}
        </NoTrackMessage>
      </Container>
    );
  }

  const { track: trackData } = track;
  const progress = (trackData.progress_ms / trackData.duration_ms) * 100;

  return (
    <Container>
      <TrackContainer>
        {trackData.album_art && (
          <AlbumArt>
            <img src={trackData.album_art} alt={`${trackData.album} アルバムアート`} />
          </AlbumArt>
        )}
        
        <TrackInfo>
          <TrackName>{trackData.name}</TrackName>
          <ArtistName>{trackData.artists.join(', ')}</ArtistName>
          <AlbumName>{trackData.album}</AlbumName>
          
          <ProgressBar>
            <ProgressFill progress={progress} />
          </ProgressBar>
          
          <TimeInfo>
            <span>{formatTime(trackData.progress_ms)}</span>
            <span>{formatTime(trackData.duration_ms)}</span>
          </TimeInfo>
          
          {trackData.artist_images && trackData.artist_images.length > 0 && (
            <ArtistImages>
              {trackData.artist_images.map((artist, index) => (
                <ArtistImage key={index}>
                  <img src={artist.image} alt={artist.name} />
                  <span>{artist.name}</span>
                </ArtistImage>
              ))}
            </ArtistImages>
          )}
          
          {trackData.external_url && (
            <SpotifyLink href={trackData.external_url} target="_blank" rel="noopener noreferrer">
              Spotifyで開く
            </SpotifyLink>
          )}
        </TrackInfo>
      </TrackContainer>
    </Container>
  );
};

export default NowPlaying; 