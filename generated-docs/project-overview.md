Last updated: 2025-11-12

# Project Overview

## プロジェクト概要
- 「Cat Window Watcher」は、アクティブなウィンドウを監視し、ユーザーの生産性をスコア化するシンプルなツールです。
- GitHubでの作業はスコアを増加させ、SNSなどの活動は減少させるなど、設定可能な正規表現パターンに基づきスコアを調整します。
- Tkinterを用いた直感的なGUIで現在のスコアと活動状況を表示し、Windows、macOS、Linuxで動作するクロスプラットフォーム対応です。

## 技術スタック
- フロントエンド: Tkinter (Pythonの標準GUIライブラリで、シンプルかつ軽量なインターフェースを提供)
- 音楽・オーディオ: 該当なし
- 開発ツール: Ruff (Pythonコードのフォーマットとリンティングを高速に実行し、コード品質を維持するためのツール)
- テスト: unittest (Python標準の単体テストフレームワーク)
- ビルドツール: TOML (設定ファイルの記述に使用される、人間が読みやすい形式の言語)
- 言語機能: Python 3.12+ (アプリケーションの主要な開発言語。OS固有のウィンドウ監視APIやAppleScript、`xdotool`/`xprop`コマンドと連携して動作)、正規表現 (ウィンドウタイトルのパターンマッチングに使用)、pywin32 (Windowsにおける高度なAPI連携のためのPythonライブラリ)
- 自動化・CI/CD: pre-commit (Gitコミット前にコードの品質チェックや整形を自動実行するためのフレームワーク)
- 開発標準: .editorconfig (異なるエディタやIDE間でコードのスタイルを一貫させるための設定ファイル)

## ファイル階層ツリー
```
📄 .editorconfig
📄 .gitignore
📄 .pre-commit-config.yaml
📁 .vscode/
  📊 settings.json
📄 LICENSE
📖 README.md
📖 USAGE.md
📄 _config.yml
📄 config.toml.example
📁 examples/
  📄 example.txt
📁 generated-docs/
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
```

## ファイル詳細説明
-   `.editorconfig`: 異なるエディタやIDE間でコードのスタイル（インデント、改行コードなど）を一貫させるための設定ファイルです。
-   `.gitignore`: Gitのバージョン管理から除外するファイルやディレクトリ（例: ログファイル、キャッシュファイルなど）を指定するファイルです。
-   `.pre-commit-config.yaml`: Gitコミット前に自動で実行されるフック（コード整形、リンティングなど）を設定するためのファイルです。
-   `.vscode/settings.json`: Visual Studio Codeエディタにおける、このプロジェクト固有の設定を定義するファイルです。
-   `LICENSE`: プロジェクトの配布および使用に関するライセンス情報が記載されたファイルです。
-   `README.md`: プロジェクトの概要、目的、機能、インストール方法、基本的な使い方、設定方法などを説明する主要なドキュメントファイルです。
-   `USAGE.md`: アプリケーションの具体的な実行方法や、コマンドラインオプションなど、より詳細な使用方法を記述したドキュメントファイルです。
-   `_config.yml`: Jekyllなどの静的サイトジェネレーターで利用される設定ファイルですが、このプロジェクト自体では直接的な機能はありません。
-   `config.toml.example`: アプリケーションの設定ファイル（`config.toml`）のサンプルです。ユーザーはこれをコピーして、自身の監視ルールを定義します。
-   `examples/example.txt`: プロジェクトの使用例やサンプルデータが含まれるディレクトリ内のファイルです。
-   `generated-docs/`: プロジェクトに関する自動生成されたドキュメントが格納されることを想定しているディレクトリです。
-   `pytest.ini`: Pythonのテストフレームワークであるpytestの設定ファイルです。
-   `ruff.toml`: Pythonの高速リンターおよびフォーマッターであるRuffの設定ファイルです。
-   `src/__init__.py`: `src` ディレクトリがPythonパッケージであることを示す空ファイルです。
-   `src/__main__.py`: `python -m src` コマンドでプロジェクトをモジュールとして実行する際のエントリーポイントとなるファイルです。
-   `src/config.py`: TOML形式の設定ファイルを読み込み、アプリケーション内で利用可能な形式に変換する役割を担うモジュールです。
-   `src/gui.py`: PythonのTkinterライブラリを使用して、スコア表示やステータス表示を行うグラフィカルユーザーインターフェース（GUI）を構築するモジュールです。
-   `src/main.py`: アプリケーション全体の主要なエントリーポイントであり、設定の読み込み、GUIの初期化、ウィンドウ監視ループの開始といった各モジュールの調整と実行を管理します。
-   `src/score_tracker.py`: 検出されたウィンドウタイトルを設定された正規表現パターンと照合し、それに基づいてスコアを計算・追跡するロジックを実装したモジュールです。
-   `src/window_monitor.py`: OS（Linux, macOS, Windows）に依存しない形で、現在アクティブなウィンドウのタイトルを取得する機能を提供するモジュールです。
-   `tests/test_config.py`: `src/config.py` モジュールの機能が正しく動作するかを検証するためのテストケースが記述されたファイルです。
-   `tests/test_dummy.py`: プロジェクトのテスト環境が適切に設定されているかを確認するためのダミーのテストファイルです。
-   `tests/test_score_tracker.py`: `src/score_tracker.py` モジュールのスコア計算およびパターンマッチングロジックを検証するためのテストケースが記述されたファイルです。
-   `tests/test_window_monitor.py`: `src/window_monitor.py` モジュールがアクティブなウィンドウタイトルを正しく取得できるかを検証するためのテストケースが記述されたファイルです。

## 関数詳細説明
-   `config.load_config(file_path: str) -> dict`:
    -   役割: 指定されたTOMLファイルから設定データを読み込み、Pythonの辞書形式で返します。
    -   引数: `file_path` (str) - 読み込む設定ファイルのパス。
    -   戻り値: (dict) - 設定内容を含む辞書。
-   `window_monitor.get_active_window_title() -> str`:
    -   役割: 現在アクティブになっているウィンドウのタイトルを、OSのAPIやコマンドを使い分けて取得します。
    -   引数: なし。
    -   戻り値: (str) - アクティブなウィンドウのタイトル文字列。
-   `score_tracker.ScoreTracker(config: list)`:
    -   役割: ウィンドウパターンとそれに対応するスコア変更値を管理し、スコアの追跡ロジックを提供します。
    -   引数: `config` (list) - ウィンドウパターン、スコア、説明を含む辞書のリスト。
    -   戻り値: なし (コンストラクタ)。
-   `score_tracker.ScoreTracker.update_score(window_title: str) -> tuple[int, str]`:
    -   役割: 与えられたウィンドウタイトルに基づいて、設定されたパターンに合致するかをチェックし、スコアを更新します。
    -   引数: `window_title` (str) - 現在アクティブなウィンドウのタイトル。
    -   戻り値: (tuple[int, str]) - 更新後の合計スコアと、マッチしたパターンの説明。
-   `gui.CatWindowWatcherGUI(score_tracker: score_tracker.ScoreTracker)`:
    -   役割: Tkinterを使用してスコアと現在の活動状況を表示するGUIを作成し、管理します。
    -   引数: `score_tracker` (ScoreTracker) - スコア追跡ロジックを提供する`ScoreTracker`インスタンス。
    -   戻り値: なし (コンストラクタ)。
-   `gui.CatWindowWatcherGUI.update_display(score: int, description: str)`:
    -   役割: GUI上のスコア表示とステータス表示を最新の情報に更新します。
    -   引数: `score` (int) - 表示する現在のスコア。`description` (str) - 表示する現在の活動説明。
    -   戻り値: なし。
-   `main.main()`:
    -   役割: アプリケーションの実行フローを制御するメイン関数です。設定の読み込み、GUIの初期化、定期的なウィンドウ監視とスコア更新のループを開始します。
    -   引数: なし。
    -   戻り値: なし。

## 関数呼び出し階層ツリー
```
main.main()
├── config.load_config()
├── score_tracker.ScoreTracker.__init__()
├── gui.CatWindowWatcherGUI.__init__()
│   └── (CatWindowWatcherGUIの内部でTkinterウィジェットを構築)
└── (メインループ: 毎秒実行)
    ├── window_monitor.get_active_window_title()
    ├── score_tracker.ScoreTracker.update_score()
    └── gui.CatWindowWatcherGUI.update_display()

---
Generated at: 2025-11-12 07:06:16 JST
