#!/usr/bin/env python3
"""
Spotify APIテストスクリプト
このスクリプトは、Spotify APIが正しく動作するかをテストします。
"""

import os
import json
import sys
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 環境変数を読み込み
load_dotenv()

def test_spotify_connection():
    """Spotify API接続をテスト"""
    print("🎵 Spotify API テスト開始")
    print("=" * 50)
    
    # 環境変数をチェック
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:3000/callback")
    
    if not client_id or not client_secret:
        print("❌ エラー: SPOTIFY_CLIENT_ID または SPOTIFY_CLIENT_SECRET が設定されていません")
        print("backend/.env ファイルを確認してください")
        return False
    
    print(f"✅ 環境変数: OK")
    print(f"   Client ID: {client_id[:10]}...")
    print(f"   Redirect URI: {redirect_uri}")
    
    try:
        # Spotifyクライアントを作成
        print("\n🔗 Spotify APIに接続中...")
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="user-read-playback-state user-read-currently-playing user-read-recently-played",
                open_browser=True  # ブラウザで認証を開く
            )
        )
        
        print("✅ Spotify API接続: 成功")
        
        # ユーザー情報を取得
        print("\n👤 ユーザー情報を取得中...")
        user = sp.current_user()
        print(f"✅ ユーザー: {user['display_name']} ({user['id']})")
        print(f"   メール: {user.get('email', 'N/A')}")
        print(f"   国: {user.get('country', 'N/A')}")
        
        # 現在再生中の曲を取得
        print("\n🎵 現在再生中の曲を取得中...")
        current_track = sp.current_user_playing_track()
        
        if current_track and current_track['is_playing']:
            track = current_track['item']
            print(f"✅ 現在再生中: {track['name']} - {track['artists'][0]['name']}")
            print(f"   アルバム: {track['album']['name']}")
            print(f"   再生時間: {current_track['progress_ms']}ms / {track['duration_ms']}ms")
            
            # アルバムアートのURL
            if track['album']['images']:
                print(f"   アルバムアート: {track['album']['images'][0]['url']}")
            
            # アーティスト情報を取得
            print("\n🎤 アーティスト情報を取得中...")
            for artist in track['artists']:
                artist_info = sp.artist(artist['id'])
                print(f"   {artist['name']}: {artist_info.get('genres', ['N/A'])[:3]}")
                if artist_info['images']:
                    print(f"   アーティスト画像: {artist_info['images'][0]['url']}")
        else:
            print("ℹ️  現在再生中の曲はありません")
        
        # 最近再生した曲を取得
        print("\n📜 最近再生した曲を取得中...")
        recent_tracks = sp.current_user_recently_played(limit=3)
        if recent_tracks['items']:
            print("✅ 最近再生した曲:")
            for i, track in enumerate(recent_tracks['items'], 1):
                track_info = track['track']
                print(f"   {i}. {track_info['name']} - {track_info['artists'][0]['name']}")
                print(f"      再生時刻: {track['played_at']}")
        else:
            print("ℹ️  最近再生した曲の履歴がありません")
        
        # プレイバック状態を取得
        print("\n🎛️  プレイバック状態を取得中...")
        playback = sp.current_playback()
        if playback:
            print(f"✅ デバイス: {playback['device']['name']}")
            print(f"   ボリューム: {playback['device']['volume_percent']}%")
            print(f"   シャッフル: {'ON' if playback['shuffle_state'] else 'OFF'}")
            print(f"   リピート: {playback['repeat_state']}")
        else:
            print("ℹ️  アクティブなデバイスがありません")
        
        print("\n" + "=" * 50)
        print("✅ すべてのテストが完了しました！")
        return True
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        print("\n考えられる原因:")
        print("1. Spotify Developer Dashboardでアプリが正しく設定されていない")
        print("2. 環境変数が正しく設定されていない")
        print("3. ネットワーク接続の問題")
        print("4. Spotifyアカウントの権限不足")
        return False

def test_api_endpoints():
    """APIエンドポイントをテスト"""
    print("\n🌐 APIエンドポイントテスト")
    print("=" * 30)
    
    import requests
    
    base_url = "http://localhost:8000"
    
    # ルートエンドポイント
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ GET /: {response.status_code}")
        print(f"   レスポンス: {response.json()}")
    except Exception as e:
        print(f"❌ GET /: エラー - {str(e)}")
    
    # 認証エンドポイント
    try:
        response = requests.get(f"{base_url}/auth")
        print(f"✅ GET /auth: {response.status_code}")
        if response.status_code == 200:
            auth_data = response.json()
            print(f"   認証URL: {auth_data.get('auth_url', 'N/A')[:50]}...")
    except Exception as e:
        print(f"❌ GET /auth: エラー - {str(e)}")
    
    # テストエンドポイント
    try:
        response = requests.get(f"{base_url}/test-spotify")
        print(f"✅ GET /test-spotify: {response.status_code}")
        if response.status_code == 200:
            test_data = response.json()
            print(f"   API接続: {test_data.get('api_connection', 'N/A')}")
            if test_data.get('current_user'):
                print(f"   ユーザー: {test_data['current_user']['display_name']}")
        else:
            print(f"   エラー: {response.text}")
    except Exception as e:
        print(f"❌ GET /test-spotify: エラー - {str(e)}")

if __name__ == "__main__":
    print("Spotify API テストツール")
    print("=" * 30)
    
    # メインのSpotify APIテスト
    success = test_spotify_connection()
    
    if success:
        print("\n" + "=" * 50)
        print("🌐 バックエンドサーバーが起動している場合、APIエンドポイントもテストできます")
        print("サーバーを起動してから Enter キーを押してください...")
        input()
        test_api_endpoints()
    
    print("\nテスト完了！") 