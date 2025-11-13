Last updated: 2025-11-14


# プロジェクト概要生成プロンプト（来訪者向け）

## 生成するもの：
- projectを3行で要約する
- プロジェクトで使用されている技術スタックをカテゴリ別に整理して説明する
- プロジェクト全体のファイル階層ツリー（ディレクトリ構造を図解）
- プロジェクト全体のファイルそれぞれの説明
- プロジェクト全体の関数それぞれの説明
- プロジェクト全体の関数の呼び出し階層ツリー

## 生成しないもの：
- Issues情報（開発者向け情報のため）
- 次の一手候補（開発者向け情報のため）
- ハルシネーションしそうなもの（例、存在しない機能や計画を勝手に妄想する等）

## 出力フォーマット：
以下のMarkdown形式で出力してください：

```markdown
# Project Overview

## プロジェクト概要
[以下の形式で3行でプロジェクトを要約]
- [1行目の説明]
- [2行目の説明]
- [3行目の説明]

## 技術スタック
[使用している技術をカテゴリ別に整理して説明]
- フロントエンド: [フロントエンド技術とその説明]
- 音楽・オーディオ: [音楽・オーディオ関連技術とその説明]
- 開発ツール: [開発支援ツールとその説明]
- テスト: [テスト関連技術とその説明]
- ビルドツール: [ビルド・パース関連技術とその説明]
- 言語機能: [言語仕様・機能とその説明]
- 自動化・CI/CD: [自動化・継続的統合関連技術とその説明]
- 開発標準: [コード品質・統一ルール関連技術とその説明]

## ファイル階層ツリー
```
[プロジェクトのディレクトリ構造をツリー形式で表現]
```

## ファイル詳細説明
[各ファイルの役割と機能を詳細に説明]

## 関数詳細説明
[各関数の役割、引数、戻り値、機能を詳細に説明]

## 関数呼び出し階層ツリー
```
[関数間の呼び出し関係をツリー形式で表現]
```
```


以下のプロジェクト情報を参考にして要約を生成してください：

## プロジェクト情報
名前: 
説明: # cat-window-watcher - Cat is watching you -

アクティブなウィンドウを監視し、あなたの作業内容に基づいてスコアを調整するシンプルでスタンドアロンなウィンドウ監視ツール。

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

開発中です。不具合があります。issueを参照ください

## ⚠️ 暫定実装についての注意

これは**テストと検証のための暫定実装**です。現在の実装は以下に焦点を当てています：
- シンプルでスタンドアロンな操作（この段階では他のアプリとの統合なし）
- 分かりやすいロジック：1秒ごとにアクティブなウィンドウタイトルをチェック
- 迅速な開発とテストを促進するための最小限の複雑さ

将来のバージョンでは最適化や統合が含まれる可能性がありますが、このバージョンはシンプルさと理解しやすさを優先しています。

## コンセプト

アプリケーションは現在アクティブなウィンドウを監視し、設定可能なパターンに基づいてスコアを調整します：
- GitHubで作業中？スコアが上がります！ 🎉
- SNSを閲覧中？スコアが下がります... 😿

The cat is watching you!

## 機能

- **シンプルなスコア表示**: クリーンなtkinter GUIで現在のスコアを表示
- **正規表現ベースのウィンドウマッチング**: 正規表現を使用してウィンドウタイトルパターンを設定
- **設定可能なスコア値**: 各パターンに対してカスタムなスコア増減量を設定
- **クロスプラットフォーム対応**: Linux、macOS、Windowsで動作
- **軽量**: 1秒に1回ウィンドウタイトルをチェック、最小限のリソース使用量

## 見た目

```
╔════════════════════════════════════════════════════════════╗
║   Cat Window Watcher - Cat is watching you -               ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║                                                            ║
║                       Score: 42                            ║
║                                                            ║
║                                                            ║
║                      GitHub (+10)                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

GUIはダークテーマで、大きなスコア表示と現在のアクティビティを表示するステータスを備えています。

## インストール

1. リポジトリをクローン：
```bash
git clone https://github.com/cat2151/cat-window-watcher.git
cd cat-window-watcher
```

2. Python 3.12以上がインストールされていることを確認：
```bash
python --version
```

3. 依存関係をインストール（必要に応じて）：
   - Linux: `xdotool` または `xprop`（通常はプリインストール済み）
   - macOS: 内蔵AppleScriptサポート
   - Windows: 内蔵APIで動作（より良いサポートのために `pywin32` をオプションで使用）

## 設定

1. 設定例をコピー：
```bash
cp config.toml.example config.toml
```

2. `config.toml`を編集してウィンドウパターンとスコアをカスタマイズ：

```toml
[[window_patterns]]
regex = "github"           # Regex pattern to match window title
score = 10                 # Score change when this window is active
description = "GitHub"     # Display description

[[window_patterns]]
regex = "twitter|x\\.com"
score = -5
description = "Twitter/X"
```

### 設定オプション

- **regex**: ウィンドウタイトルにマッチする正規表現パターン（大文字小文字を区別しない）
- **score**: パターンがマッチしたときにスコアに追加する整数値（負の値も可能）
- **description**: ステータスエリアに表示される人間が読める説明

## 使用法

アプリケーションを実行：
```bash
# 方法1: スクリプトを直接実行
python src/main.py

# 方法2: モジュールとして実行
python -m src

# 方法3: カスタム設定ファイルで実行
python src/main.py --config my_config.toml
python src/main.py -c my_config.toml
```

GUIには以下が表示されます：
- 現在のスコアを大きなテキストで表示
- 現在マッチしたパターンまたはウィンドウタイトルを表示するステータス
- 1秒ごとに自動更新

## 例

### 例1: 生産性の追跡
```toml
[[window_patterns]]
regex = "github|gitlab"
score = 10
description = "コーディング"

[[window_patterns]]
regex = "twitter|facebook|instagram"
score = -5
description = "ソーシャルメディア"
```

### 例2: 勉強時間
```toml
[[window_patterns]]
regex = "pdf|documentation|docs"
score = 8
description = "読書"

[[window_patterns]]
regex = "youtube|netflix"
score = -10
description = "エンターテイメント"
```

## 開発

### テストの実行
```bash
python -m unittest discover tests/ -v
```

### コードフォーマット
コミット前にコードをフォーマット：
```bash
ruff format src/ tests/
ruff check --fix src/ tests/
```

### リンティング
コード品質の検証：
```bash
ruff format --check src/ tests/
ruff check src/ tests/
```

## アーキテクチャ

アプリケーションはいくつかのモジュールから構成されています：

- **config.py**: TOML設定の読み込みと管理
- **window_monitor.py**: クロスプラットフォームなウィンドウタイトル検出
- **score_tracker.py**: ウィンドウタイトルをパターンにマッチさせ、スコアを追跡
- **gui.py**: tkinterベースのスコア表示インターフェース
- **main.py**: アプリケーションのエントリポイントとオーケストレーション

## プラットフォーム固有の注意事項

### Linux
`xdotool` または `xprop` が必要：
```bash
sudo apt-get install xdotool  # Debian/Ubuntu
```

### macOS
内蔵AppleScriptを使用。追加の依存関係は不要。

### Windows
内蔵Windows APIで動作。より良い互換性のためにインストール：
```bash
pip install pywin32
```

## ライセンス

詳細はLICENSEファイルをご覧ください。

*Big Brother is watching you. But this time, it's a cat. 🐱*


依存関係:
{}

## ファイル階層ツリー
📄 .editorconfig
📄 .gitignore
📄 .pre-commit-config.yaml
📁 .vscode/
  📊 settings.json
📄 LICENSE
📖 README.ja.md
📖 README.md
📄 _config.yml
📄 config.toml.example
📁 examples/
  📄 example.txt
📁 generated-docs/
📁 issue-notes/
  📖 4.md
📄 pytest.ini
📄 ruff.toml
📁 src/
  📄 __init__.py
  📄 __main__.py
  📄 config.py
  📄 gui.py
  📄 main.py
  📄 score_tracker.py
  📄 window_monitor.py
📁 tests/
  📄 test_config.py
  📄 test_dummy.py
  📄 test_score_tracker.py
  📄 test_window_monitor.py

## ファイル詳細分析


## 関数呼び出し階層
関数呼び出し階層を分析できませんでした

## プロジェクト構造（ファイル一覧）
.vscode/settings.json
README.ja.md
README.md
issue-notes/4.md

上記の情報を基に、プロンプトで指定された形式でプロジェクト概要を生成してください。
特に以下の点を重視してください：
- 技術スタックは各カテゴリごとに整理して説明
- ファイル階層ツリーは提供された構造をそのまま使用
- ファイルの説明は各ファイルの実際の内容と機能に基づく
- 関数の説明は実際に検出された関数の役割に基づく
- 関数呼び出し階層は実際の呼び出し関係に基づく


---
Generated at: 2025-11-14 07:06:06 JST
