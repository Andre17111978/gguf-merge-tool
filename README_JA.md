GGUF Merge Tool v10.0
https://badge.fury.io/py/gguf-merge-tool.svg
https://img.shields.io/badge/python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg

プロフェッショナルなGUI + CLIツール - Hugging FaceからシャーディングされたGGUFモデルをダウンロード、検証、マージするためのツールです。

✨ バージョン10.0の新機能
機能	説明
プログレスバーの修正	ハッシュ検証とマージ操作中に進捗がスムーズかつ正確に表示されるようになりました
ローカルファイルの読み込み	「ローカル」ボタンでディスク上のGGUFファイルが含まれるフォルダを選択し、ダウンロードなしで作業できます
リポジトリ履歴	リポジトリ入力フィールドのドロップダウンリスト — 過去10件のクエリを保存
🚀 主な機能
ダウンロード Hugging FaceからのGGUFファイル（レジューム機能付き）。

整合性検証 ダウンロードしたファイルのSHA-256チェック。

マージ llama-gguf-splitを使用して分割ファイルを1つのGGUFファイルに結合。

グループ化 量子化とベース名によるファイルの自動グループ化。

マルチスレッド ダウンロード（コア数を自動検出）。

リアルタイムETA ダウンロード中の速度（MB/s）と残り時間を表示。

CLIモード 自動化に対応。

永続化 セッション間でのトークンとllama.cppパスの保存。

📦 インストール
PyPIから（推奨）
bash
pip install gguf-merge-tool
インストール後、以下の2つのコマンドが使用可能になります：

gguf-merge-gui — グラフィカルインターフェースを起動

gguf-merge — CLIモードを起動

ソースから
bash
git clone https://github.com/Andre17111978/gguf-merge-tool.git
cd gguf-merge-tool
pip install -r requirements.txt
python gguf_merge_tool.py
🖥️ 使用方法（GUI）
bash
gguf-merge-gui
# または
python gguf_merge_tool.py
ステップバイステップのインターフェース：
フィールド	説明
リポジトリ	Hugging FaceのリポジトリIDを入力（例：unsloth/Qwen3.5-122B-A10B-GGUF）。
履歴は自動的に過去10件のクエリを保存します。
ブランチ	通常はmain。
トークン	オプション。プライベートリポジトリ用（形式：hf_xxxxxxxxxxxxxxxxxx）。
ダウンロードフォルダ	ファイルの保存先。
llama.cppパス	llama-gguf-splitが含まれるフォルダを指定（マージに必要）。
ファイル	チェックボックス付きのGGUFファイル一覧。量子化タイプで自動グループ化されます。
コントロールボタン：
ボタン	機能
読み込み	リポジトリからファイル一覧を取得。
ローカル	ディスク上のGGUFフォルダを選択。
すべて選択 / すべてダウンロード	一括操作。
ダウンロード	選択したファイルをダウンロード。
検証	SHA-256ハッシュをチェック。
マージ	選択したパーツを結合。
⌨️ 使用方法（CLI）
特定のファイルをダウンロード
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models -f model-00001-of-00003.gguf model-00002-of-00003.gguf
リポジトリ全体をダウンロード
bash
gguf-merge download -r unsloth/Qwen3.5-122B-A10B-GGUF -d ./models
トークンを使用してダウンロード（プライベートリポジトリ）
bash
gguf-merge download -r your-username/your-private-model -d ./models -t hf_xxxxxxxxxxxxxxxxxx
パーツをマージ
bash
gguf-merge merge -d ./models -o ./models/merged_model.gguf -f
CLI引数
downloadコマンド：

引数	説明
-d, --dir	保存フォルダ（必須）
-r, --repo	リポジトリID（必須）
-b, --branch	ブランチ（デフォルト：main）
-t, --token	Hugging Faceトークン
-f, --files	ダウンロードするファイルのリスト
mergeコマンド：

引数	説明
-d, --dir	パーツが入っているフォルダ（必須）
-o, --output	出力ファイルのパス
-f, --force	既存ファイルを上書き
⚙️ システム要件
Python >= 3.8

依存関係（自動インストール）：
huggingface_hub >= 0.20.0

tqdm >= 4.60.0

requests >= 2.28.0

gguf >= 0.1.0（オプション、メタデータ読み取り用）

追加で必要なツール：
llama-gguf-split（llama.cppリリースページからダウンロード）

🛠️ トラブルシューティング
llama-gguf-splitが見つからない
llama.cppリリースページからダウンロード

tools/フォルダに配置するか、GUI設定でパスを指定

HTTP 401/403（認証エラー/アクセス禁止）
有効なHugging Faceトークンを入力

トークンがリポジトリへのアクセス権を持っていることを確認

ディスク容量が不足している
容量を空けるか、ダウンロードフォルダを変更

コード内のDISK_SPACE_MARGINを変更可能（デフォルト：1.1 = 10%のバッファ）

LinuxでGUIが起動しない
bash
sudo apt-get install python3-tk  # Debian/Ubuntu
brew install python-tk           # macOS
📝 ライセンス
MITライセンスの下で配布されています。詳細はLICENSEファイルをご覧ください。

🙏 謝辞
llama.cpp — マージユーティリティを提供

Hugging Face — モデルをホスティング

コミュニティの皆様 — テストとアイデアを提供

⭐ プロジェクトをサポート
このツールがお役に立ったなら、GitHubでスターを付けてください！

❤️ AIコミュニティのために作られました