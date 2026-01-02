Last updated: 2026-01-03

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、ユーザーの作業内容に応じてスコアを調整するツールです。
- 設定可能な正規表現パターンに基づき、生産的な作業にはスコアを加算し、非生産的な活動には減点します。
- シンプルなTkinter GUIで現在のスコアと活動を表示し、集中力の維持をサポートします。

## 技術スタック
- フロントエンド: **tkinter** (Python標準のGUIライブラリで、スコアと活動状況を表示するシンプルなグラフィカルインターフェースを構築します。), **pywin32** (Windows環境において、より高度なシステムAPIアクセスやウィンドウ操作機能を提供し、クロスプラットフォーム対応を強化します。)
- 音楽・オーディオ: (該当する技術は使用されていません)
- 開発ツール: **Git** (プロジェクトのバージョン管理に使用), **ruff** (Pythonコードのフォーマットとリンティングを高速に実行し、コード品質と統一性を保ちます。), **pre-commit** (コミット前に自動的にコードフォーマットやリンティングを実行するGitフックを管理します。)
- テスト: **unittest** (Python標準のテストフレームワークで、各モジュールの単体テストを記述・実行します。), **pytest** (柔軟なテスト記述と実行を可能にするテストフレームワークで、`pytest.ini`によりテスト設定が管理されます。)
- ビルドツール: (Pythonスクリプトとして直接実行されるため、特定のビルドツールは使用されていません)
- 言語機能: **Python 3.12+** (アプリケーションの基盤となるプログラミング言語。最新のPython機能を利用しています。), **正規表現 (reモジュール)** (ウィンドウタイトルをマッチングするためのパターン定義に活用されます。)
- 自動化・CI/CD: **pre-commit** (開発ワークフローにおいて、コードのコミット前に品質チェックを自動化します。)
- 開発標準: **ruff** (コードスタイルと潜在的なエラーをチェックし、プロジェクト全体のコード品質を均一に保ちます。), **.editorconfig** (異なるエディタやIDE間でコードスタイルの一貫性を維持するための設定ファイルです。)

## ファイル階層ツリー
```
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
  📖 11.md
  📖 12.md
  📖 13.md
  📖 14.md
  📖 15.md
  📖 16.md
  📖 21.md
  📖 26.md
  📖 27.md
  📖 29.md
  📖 31.md
  📖 33.md
  📖 34.md
  📖 37.md
  📖 39.md
  📖 4.md
  📖 40.md
  📖 43.md
  📖 6.md
  📖 8.md
  📖 9.md
📄 pytest.ini
📄 ruff.toml
📁 src/
  📄 __init__.py
  📄 __main__.py
  📄 config.py
  📄 constants.py
  📄 gui.py
  📄 main.py
  📄 score_tracker.py
  📄 window_monitor.py
📁 tests/
  📄 test_config.py
  📄 test_dummy.py
  📄 test_gui.py
  📄 test_score_colors.py
  📄 test_score_tracker.py
  📄 test_window_monitor.py
```

## ファイル詳細説明
-   `.editorconfig`: IDEやエディタ全体で一貫したコーディングスタイル（インデント、改行など）を定義するための設定ファイル。
-   `.gitignore`: Gitがバージョン管理の対象外とするファイルやディレクトリを指定するファイル。
-   `.pre-commit-config.yaml`: `pre-commit`フレームワークの設定ファイル。コミット前に自動実行されるスクリプトやツール（例: フォーマッター、リンター）を定義します。
-   `.vscode/settings.json`: Visual Studio Codeエディタのワークスペース固有の設定を定義するファイル。
-   `LICENSE`: このプロジェクトのソフトウェアライセンス情報が記載されたファイル。
-   `README.ja.md`, `README.md`: プロジェクトの概要、インストール方法、使用方法、機能などを説明するドキュメント（日本語版と英語版）。
-   `_config.yml`: Jekyllなどの静的サイトジェネレーターで利用される設定ファイル。
-   `config.toml.example`: `config.toml`を作成する際のテンプレートとして使用される設定例ファイル。ウィンドウパターンやスコア設定のカスタマイズ方法が示されています。
-   `examples/example.txt`: プロジェクト内で使用されるかもしれない、例示目的のテキストファイル。
-   `generated-docs/`: 自動生成されたドキュメントを格納するためのディレクトリ。
-   `issue-notes/`: 開発中の特定のIssueに関するメモや詳細な議論を記録したMarkdownファイルのコレクション。
-   `pytest.ini`: `pytest`テストフレームワークの設定ファイル。テストの実行方法や検出に関するオプションを定義します。
-   `ruff.toml`: `ruff`LinterおよびFormatterの設定ファイル。コードの検査ルールやフォーマットルールをカスタマイズします。
-   `src/__init__.py`: `src`ディレクトリがPythonパッケージであることを示すファイル。
-   `src/__main__.py`: `python -m src`のようにモジュールとして実行された際に起動するエントリポイント。通常は`main.py`の処理を呼び出します。
-   `src/config.py`: TOML形式の設定ファイル（`config.toml`）を読み込み、アプリケーション内で使用可能な形式で管理する役割を担うモジュール。
-   `src/constants.py`: アプリケーション全体で共有される不変の定数（例: アプリケーション名、デフォルト値など）を定義するモジュール。
-   `src/gui.py`: `tkinter`ライブラリを使用して、アプリケーションのユーザーインターフェース（スコア表示、アクティビティ表示など）を構築し、管理するモジュール。
-   `src/main.py`: アプリケーションの主要なエントリポイント。他のモジュール（`config`、`window_monitor`、`score_tracker`、`gui`）を初期化し、メインの監視ループとUIの更新処理をオーケストレートします。
-   `src/score_tracker.py`: アクティブなウィンドウタイトルを監視し、設定されたパターンに基づいてスコアを計算・更新するビジネスロジックを実装したモジュール。
-   `src/window_monitor.py`: OS（Linux, macOS, Windows）に依存せずに、現在アクティブなウィンドウのタイトルを取得する機能を提供するモジュール。
-   `tests/`: プロジェクトの各モジュールのテストコードを格納するディレクトリ。
    -   `test_config.py`: `config.py`モジュールの機能（設定の読み込み、解析など）を検証するテストファイル。
    -   `test_dummy.py`: テストディレクトリの動作確認や初期設定のためのダミーテストファイル。
    -   `test_gui.py`: `gui.py`モジュールのGUIコンポーネントや表示ロジックをテストするファイル。
    -   `test_score_colors.py`: スコアの変化に応じてGUIの表示色が正しく変更されるかをテストするファイル。
    -   `test_score_tracker.py`: `score_tracker.py`モジュールのスコア計算ロジックやパターンマッチング機能を検証するテストファイル。
    -   `test_window_monitor.py`: `window_monitor.py`モジュールのウィンドウタイトル取得機能が正しく動作するかをテストするファイル。

## 関数詳細説明
-   `main()` in `src/main.py`:
    -   役割: アプリケーションの主要な実行フローを制御します。設定の読み込み、GUIの初期化、ウィンドウ監視とスコア更新のメインループの開始を行います。
    -   引数: なし。
    -   戻り値: なし。
    -   機能: アプリケーション全体の初期設定と実行を管理するエントリポイントです。
-   `run_watcher()` in `src/main.py`:
    -   役割: ウィンドウ監視とスコア更新を周期的に実行するメインループを処理します。
    -   引数: `config` (設定オブジェクト), `gui` (GUIオブジェクト), `score_tracker` (スコアトラッカーオブジェクト), `window_monitor` (ウィンドウモニターオブジェクト)。
    -   戻り値: なし。
    -   機能: 1秒ごとにアクティブなウィンドウタイトルを取得し、スコアを更新し、GUIを更新します。
-   `load_config(filepath)` in `src/config.py`:
    -   役割: 指定されたパスからTOML形式の設定ファイルを読み込み、解析します。
    -   引数: `filepath` (設定ファイルへのパスを示す文字列)。
    -   戻り値: 設定内容を格納した辞書またはオブジェクト。
    -   機能: アプリケーションの挙動をカスタマイズするための設定値を外部ファイルから取得します。
-   `get_active_window_title()` in `src/window_monitor.py`:
    -   役割: 現在フォーカスされているアクティブなウィンドウのタイトルを取得します。
    -   引数: なし。
    -   戻り値: アクティブなウィンドウのタイトルを示す文字列、またはタイトルが取得できない場合は空文字列。
    -   機能: OSのAPIを活用して、現在ユーザーが操作しているウィンドウを特定します。
-   `update_score(window_title)` in `src/score_tracker.py`:
    -   役割: 渡されたウィンドウタイトルに基づいてスコアを計算し、現在のスコアを更新します。
    -   引数: `window_title` (現在アクティブなウィンドウのタイトル文字列)。
    -   戻り値: `(新しいスコア, 適用された説明, スコア変化量)`のタプル。
    -   機能: 設定された正規表現パターンとマッチさせ、対応するスコア増減量を適用します。
-   `get_current_score()` in `src/score_tracker.py`:
    -   役割: 現在のスコアを取得します。
    -   引数: なし。
    -   戻り値: 現在のスコアを示す整数値。
    -   機能: スコアトラッカーが保持している現在のスコア値を返します。
-   `create_gui(initial_score, update_callback)` in `src/gui.py`:
    -   役割: `tkinter`を使用して、スコアとアクティビティを表示するメインのGUIウィンドウを作成し、表示します。
    -   引数: `initial_score` (初期表示スコア), `update_callback` (GUIの更新をトリガーするためのコールバック関数)。
    -   戻り値: GUIオブジェクト。
    -   機能: ユーザーインターフェースを初期化し、イベントループを開始します。
-   `update_score_display(score, activity_description, score_color)` in `src/gui.py`:
    -   役割: GUIウィンドウ上のスコア表示とアクティビティ説明を更新します。
    -   引数: `score` (更新するスコア値), `activity_description` (現在の活動を示す説明), `score_color` (スコア表示の色)。
    -   戻り値: なし。
    -   機能: リアルタイムでスコアと関連情報をユーザーに視覚的にフィードバックします。

## 関数呼び出し階層ツリー
```
main() in src/main.py
├── load_config() in src/config.py (設定ファイルを読み込む)
├── create_gui() in src/gui.py (GUIを初期化し表示)
│   └── update_score_display() in src/gui.py (初期スコアを表示)
└── run_watcher() in src/main.py (監視ループを開始)
    ├── get_active_window_title() in src/window_monitor.py (アクティブウィンドウタイトルを取得)
    ├── update_score() in src/score_tracker.py (取得したタイトルでスコアを更新)
    │   └── get_current_score() in src/score_tracker.py (現在のスコアを取得)
    └── update_score_display() in src/gui.py (更新されたスコアと活動をGUIに表示)

---
Generated at: 2026-01-03 07:05:56 JST
