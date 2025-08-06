# Now-Playing-Realtime-Widget

Spotify APIを使用してリアルタイムで再生中の曲を共有するWebアプリケーション

## 機能
- Spotifyで再生中の曲をリアルタイムで取得
- 曲名、アーティスト名、ジャケット写真、アーティスト写真を表示
- WebSocketを使用したリアルタイム更新
- Reactフロントエンド + Pythonバックエンド

## セットアップ

### 1. Spotify API設定
1. [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)でアプリを作成
2. Client IDとClient Secretを取得
3. Redirect URIを設定（例: `http://localhost:3000/callback`）

### 2. バックエンド（Python）
```bash
cd backend
# 仮想環境を作成（初回のみ）
python3 -m venv venv

# 仮想環境をアクティベート
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows

# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを起動
python main.py

# または、起動スクリプトを使用（macOS/Linux）
./start.sh
```

### 3. フロントエンド（React）
```bash
cd frontend
npm install
npm start
```

## 環境変数
`.env`ファイルを作成し、以下を設定：
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/callback
```

## 使用方法
1. バックエンドとフロントエンドを起動
2. ブラウザで `http://localhost:3000` にアクセス
3. Spotifyアカウントでログイン
4. 再生中の曲がリアルタイムで表示されます
