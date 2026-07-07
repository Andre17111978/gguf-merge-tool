GGUF Merge Tool v9.2

Hugging Faceからシャード化されたGGUFモデルをダウンロード、検証、マージするためのプロフェッショナルなGUI + CLIツール
目次

    機能

    クイックスタート

    インストール

    CLIの使用方法

    GUIの使用方法

    設定

    要件

    トラブルシューティング

    パフォーマンスのヒント

    技術的詳細

    ライセンス

    謝辞

    サポート

機能

モダンなGUI - Tkinterベースのインターフェース、スクロール可能なファイルリスト、マウスホイールサポート

スマートグループ化 - 量子化タイプ別に自動グループ化 (Q4_K_M, Q5_K_Sなど)

レジュームダウンロード - HTTP Rangeリクエストとスマートフォールバック保護 (200 vs 206処理)

並列ダウンロード - 設定可能なスレッド数 (CPUコアを自動検出)

ハッシュ検証 - HF LFSメタデータを使用したSHA256検証

スマートマージ - llama.cppのllama-gguf-splitを使用

CLIサポート - 自動化のためのdownloadとmergeサブコマンド

スマート検出 - 一般的な場所でllama-gguf-splitを自動検出

パス永続化 - セッション間でllama.cppのパスを保存

リトライロジック - 指数バックオフによる自動リトライ (3回)

リアルタイムETA - 速度(MB/s)と推定残り時間を表示

多言語 - 6言語のドキュメント
クイックスタート
Windows

依存関係をインストール:
pip install huggingface_hub tqdm requests

llama-gguf-splitをダウンロード: https://github.com/ggerganov/llama.cpp/releases

ツールを実行:
python gguf_merge_tool.py
Linux / macOS

依存関係をインストール:
pip install huggingface_hub tqdm requests

ツールを実行:
python3 gguf_merge_tool.py
インストール
ソースからインストール (推奨)

リポジトリをクローン:
git clone https://github.com/yourusername/gguf-merge-tool.git
cd gguf-merge-tool

依存関係をインストール:
pip install -r requirements.txt

ツールを実行:
python src/gguf_merge_tool.py
PyPIから (近日公開)

pip install gguf-merge-tool
gguf-merge-gui
Windowsユーザー: 必要なバイナリ

llama.cppリリースからllama-gguf-split.exeをダウンロード
以下のいずれかの場所に配置:

    tools/llama-gguf-split.exe

    bin/llama-gguf-split.exe

    またはGUI設定でパスを指定

CLIの使用方法
特定のファイルをダウンロード

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f Qwen3.5-122B-A10B-Q4_K_M-00001-of-00008.gguf Qwen3.5-122B-A10B-Q4_K_M-00002-of-00008.gguf
リポジトリ全体をダウンロード

python src/gguf_merge_tool.py download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
認証付きダウンロード (プライベートリポジトリ)

python src/gguf_merge_tool.py download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
パーツをマージ

python src/gguf_merge_tool.py merge -d ./models -o ./models/merged_model.gguf -f
CLI引数リファレンス

コマンド: download
-d, --dir - ファイルを保存するディレクトリ - 必須: はい
-r, --repo - Hugging FaceリポジトリID - 必須: はい
-b, --branch - リポジトリブランチ (デフォルト: main) - 必須: いいえ
-t, --token - HFアクセストークン - 必須: いいえ
-f, --files - ダウンロードするファイルのリスト - 必須: いいえ

コマンド: merge
-d, --dir - パーツがあるディレクトリ - 必須: はい
-o, --output - 出力ファイルのパス - 必須: いいえ
-f, --force - 既存ファイルを上書き - 必須: いいえ
GUIの使用方法
ステップ1: リポジトリを読み込む

Hugging FaceリポジトリIDを入力 (例: unsloth/Qwen3.5-122B-A10B-GGUF)
ブランチを入力 (デフォルト: main)
HFトークンを入力 (プライベートリポジトリに必要)
"読み込み"ボタンをクリック
ステップ2: ファイルを選択

ファイルは量子化タイプ別に自動グループ化
"すべて選択"をクリックして全ファイルを選択
またはチェックボックスで個別ファイルを選択
ステップ3: ダウンロード

"ダウンロード"または"すべてダウンロード"をクリック
リアルタイムで進捗を監視:

    プログレスバーはパーセンテージを表示

    ステータスバー表示: [1/4] filename.gguf: 45% | 4.5 MB/s | ETA: 2h 15m

ステップ4: 検証 (オプションだが推奨)

"検証"ボタンをクリック
ツールがHFメタデータに対してSHA256ハッシュを検証
すべてのハッシュが一致すると成功メッセージを表示
ステップ5: マージ (オプション)

少なくとも2つのパーツを選択 (チェックボックス)
"マージ"ボタンをクリック
ツールがllama-gguf-split --mergeを実行
出力ファイルは正しいベース名で保存
設定
llama.cppパス

GUIで"llama.cppへのパス"を探す:
"検索"をクリックして自動検出
または"参照"をクリックして手動選択
パスはllama_path.txtに保存され永続化
スレッド設定

コード内のJOBS定数を調整 (デフォルト: min(4, os.cpu_count() or 2)):
gguf_merge_tool.py内
JOBS = min(4, os.cpu_count() or 2) - この値を変更
ディスクスペースマージン

DISK_SPACE_MARGINを変更 (デフォルト: 1.1 = 10%余分):
DISK_SPACE_MARGIN = 1.1
ダウンロードチャンクサイズ

CHUNK_SIZEを変更 (デフォルト: 1 MB):
CHUNK_SIZE = 1024 * 1024
要件

Python >= 3.8
huggingface_hub >= 0.20.0
tqdm >= 4.60.0
requests >= 2.28.0
gguf >= 0.1.0 (オプション、メタデータ読み取り用)
llama-gguf-split (llama.cppから)
インストール確認

python -c "import huggingface_hub, tqdm, requests; print('すべての依存関係がインストールされました')"
トラブルシューティング
llama-gguf-splitが見つからない

llama.cppリリースからダウンロード
tools/フォルダに配置するかGUIでパスを指定
HTTP 401 UnauthorizedまたはHTTP 403 Forbidden

Hugging Faceトークンを入力
トークンがリポジトリへの読み取りアクセス権を持っていることを確認
トークン形式: hf_xxxxxxxxxxxxxxxxxx
ディスクスペース不足

ディスクスペースを解放 (マージに10%の余裕が必要)
ダウンロードディレクトリを別のドライブに変更
DISK_SPACE_MARGINを使用してバッファを調整
ダウンロードが0%で停止

インターネット接続を確認
トークンが正しいか確認
リポジトリがプライベートか確認
リポジトリが存在するか確認
再開後にファイルが破損

ツールにはRangeフォールバック保護が組み込まれている
サーバーがRangeをサポートしない場合 (206ではなく200を返す)、ダウンロードを最初から開始
これはファイル破損を防ぐための意図的な動作
GUIが起動しない

Tkinterがインストールされているか確認 (通常Pythonに含まれる)
Linuxの場合: sudo apt-get install python3-tk
macOSの場合: brew install python-tk
パフォーマンスのヒント

多くの小ファイル - デフォルトスレッドを維持 (4)
少数の大ファイル - スレッドを8に増やす
ネットワークが遅い - スレッドを2に減らす
高速NVMe SSD - デフォルト維持または増加
ネットワーク切断 - ツールが自動的に再開
技術的詳細
ダウンロードフロー

HFリポジトリからファイルリストを取得 (サイズとハッシュを含む)
ユーザーがダウンロードするファイルを選択
ディスクスペースをチェック - 不足している場合は中止
Rangeリクエストによる並列ダウンロードと再開
スマートRangeフォールバック (200 vs 206処理)
速度計算によるリアルタイム進捗
ダウンロード後のSHA256検証
llama-gguf-splitによるマージ
ETA計算

ETA = (総バイト数 - ダウンロード済みバイト数) / 現在の速度
サポートされている量子化

F16, F32, Q8_0, Q6_K, Q5_K_M, Q5_K_S, Q4_K_M, Q4_K_S, Q3_K_M, Q3_K_S, Q2_K, IQ4_XS, IQ3_XS, IQ2_XS, IQ1_S
ライセンス

MITライセンス - 詳細はLICENSEファイルを参照。
謝辞

llama.cpp (マージユーティリティ)
Hugging Face (モデルホスティング)
Python Tkinter (GUI)
サポート

問題: GitHub Issues
ディスカッション: GitHub Discussions
このプロジェクトにスターを付ける

このツールが役に立ったら、GitHubでスターを付けてください！

❤️を込めてAIコミュニティへ