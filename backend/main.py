import os
import json
import asyncio
from typing import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import uvicorn

# 環境変数を読み込み
load_dotenv()

app = FastAPI(title="Spotify Now Playing API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket接続を管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # 接続が切れた場合は削除
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Spotify API設定
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:3000/callback")

# Spotify OAuth設定
SCOPES = [
    "user-read-playback-state",
    "user-read-currently-playing",
    "user-read-recently-played"
]

def create_spotify_client():
    """Spotifyクライアントを作成"""
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=" ".join(SCOPES),
            open_browser=False
        )
    )

def get_current_track_info(sp):
    """現在再生中の曲の情報を取得"""
    try:
        current_track = sp.current_user_playing_track()
        
        if not current_track or not current_track['is_playing']:
            return {
                "is_playing": False,
                "message": "現在再生中の曲はありません"
            }
        
        track = current_track['item']
        if not track:
            return {
                "is_playing": False,
                "message": "曲の情報を取得できませんでした"
            }
        
        # アーティスト情報を取得
        artists = track['artists']
        artist_names = [artist['name'] for artist in artists]
        artist_images = []
        
        # 各アーティストの画像を取得
        for artist in artists:
            artist_info = sp.artist(artist['id'])
            if artist_info['images']:
                artist_images.append({
                    'name': artist['name'],
                    'image': artist_info['images'][0]['url']
                })
        
        return {
            "is_playing": True,
            "track": {
                "name": track['name'],
                "artists": artist_names,
                "album": track['album']['name'],
                "album_art": track['album']['images'][0]['url'] if track['album']['images'] else None,
                "artist_images": artist_images,
                "duration_ms": track['duration_ms'],
                "progress_ms": current_track['progress_ms'],
                "external_url": track['external_urls']['spotify']
            }
        }
    except Exception as e:
        return {
            "is_playing": False,
            "error": str(e),
            "message": "曲の情報を取得中にエラーが発生しました"
        }

@app.get("/")
async def root():
    return {"message": "Spotify Now Playing API"}

@app.get("/auth")
async def auth():
    """Spotify認証URLを取得"""
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=" ".join(SCOPES)
    )
    auth_url = sp_oauth.get_authorize_url()
    return {"auth_url": auth_url}

@app.get("/callback")
async def callback(code: str):
    """Spotify認証コールバック"""
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=" ".join(SCOPES)
    )
    
    try:
        token_info = sp_oauth.get_access_token(code)
        return {"success": True, "token": token_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/current-track")
async def get_current_track():
    """現在再生中の曲の情報を取得（REST API）"""
    try:
        sp = create_spotify_client()
        track_info = get_current_track_info(sp)
        return track_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-spotify")
async def test_spotify():
    """Spotify APIのテスト用エンドポイント"""
    try:
        sp = create_spotify_client()
        
        # 基本的なAPI接続テスト
        test_results = {
            "api_connection": "OK",
            "current_user": None,
            "current_track": None,
            "recent_tracks": None,
            "errors": []
        }
        
        # ユーザー情報を取得
        try:
            user = sp.current_user()
            test_results["current_user"] = {
                "id": user['id'],
                "display_name": user['display_name'],
                "email": user.get('email', 'N/A'),
                "country": user.get('country', 'N/A')
            }
        except Exception as e:
            test_results["errors"].append(f"ユーザー情報取得エラー: {str(e)}")
        
        # 現在再生中の曲を取得
        try:
            current_track = sp.current_user_playing_track()
            if current_track:
                test_results["current_track"] = {
                    "is_playing": current_track.get('is_playing', False),
                    "track_name": current_track['item']['name'] if current_track['item'] else None,
                    "artist_name": current_track['item']['artists'][0]['name'] if current_track['item'] and current_track['item']['artists'] else None,
                    "album_name": current_track['item']['album']['name'] if current_track['item'] else None,
                    "progress_ms": current_track.get('progress_ms', 0),
                    "duration_ms": current_track['item']['duration_ms'] if current_track['item'] else None
                }
            else:
                test_results["current_track"] = "再生中の曲なし"
        except Exception as e:
            test_results["errors"].append(f"現在の曲取得エラー: {str(e)}")
        
        # 最近再生した曲を取得
        try:
            recent_tracks = sp.current_user_recently_played(limit=5)
            test_results["recent_tracks"] = [
                {
                    "track_name": track['track']['name'],
                    "artist_name": track['track']['artists'][0]['name'],
                    "played_at": track['played_at']
                }
                for track in recent_tracks['items']
            ]
        except Exception as e:
            test_results["errors"].append(f"最近の曲取得エラー: {str(e)}")
        
        return test_results
        
    except Exception as e:
        return {
            "api_connection": "ERROR",
            "error": str(e),
            "message": "Spotify API接続に失敗しました"
        }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocketエンドポイント"""
    await manager.connect(websocket)
    
    try:
        sp = create_spotify_client()
        
        while True:
            # 現在の曲の情報を取得
            track_info = get_current_track_info(sp)
            
            # WebSocketで送信
            await manager.send_personal_message(
                json.dumps(track_info, ensure_ascii=False),
                websocket
            )
            
            # 5秒待機
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 