#!/bin/bash

echo "🎵 Spotify Now Playing Widget セットアップ"
echo "=========================================="

# バックエンドのセットアップ
echo "📦 バックエンドの仮想環境を作成中..."
cd backend

# 仮想環境が存在しない場合は作成
if [ ! -d "venv" ]; then
    echo "仮想環境を作成しています..."
    python3 -m venv venv
else
    echo "仮想環境は既に存在します"
fi

# 仮想環境をアクティベート
echo "仮想環境をアクティベート中..."
source venv/bin/activate

# 依存関係をインストール
echo "依存関係をインストール中..."
pip install -r requirements.txt

# 仮想環境を非アクティベート
deactivate

cd ..

# フロントエンドのセットアップ
echo "📦 フロントエンドの依存関係をインストール中..."
cd frontend
npm install
cd ..

echo ""
echo "✅ セットアップ完了！"
echo ""
echo "次の手順を実行してください："
echo ""
echo "1. Spotify Developer Dashboard (https://developer.spotify.com/dashboard) でアプリを作成"
echo "2. Client IDとClient Secretを取得"
echo "3. Redirect URIを 'http://localhost:3000/callback' に設定"
echo "4. backend/.env ファイルを作成し、環境変数を設定："
echo "   SPOTIFY_CLIENT_ID=your_client_id"
echo "   SPOTIFY_CLIENT_SECRET=your_client_secret"
echo "   SPOTIFY_REDIRECT_URI=http://localhost:3000/callback"
echo ""
echo "5. アプリケーションを起動："
echo "   - バックエンド: cd backend && source venv/bin/activate && python main.py"
echo "   - フロントエンド: cd frontend && npm start"
echo ""
echo "6. ブラウザで http://localhost:3000 にアクセス" 