Last updated: 2026-01-06

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、生産的な作業を促すシンプルでスタンドアロンなツールです。
- ウィンドウタイトルに設定されたパターンに基づいてスコアをリアルタイムで調整・表示します。
- カスタマイズ可能な設定と軽量なクロスプラットフォーム対応GUIを提供し、集中力向上を支援します。

## 技術スタック
- フロントエンド:
  - `tkinter`: Pythonの標準GUIライブラリで、シンプルでクリーンなユーザーインターフェースを提供します。
- 音楽・オーディオ:
  - 該当する技術は使用されていません。
- 開発ツール:
  - `Python 3.12+`: アプリケーションの主要な開発言語および実行環境です。
  - `Git`: ソースコードの変更履歴を管理するバージョン管理システムです。
  - `pre-commit`: コミット前にコードの品質チェックやフォーマットを自動実行するフック管理ツールです。
  - `ruff`: 高速なPythonリンターおよびフォーマッターで、コード品質の維持と統一されたコーディングスタイルを保証します。
  - `unittest`: Python標準の単体テストフレームワークで、各モジュールの機能が正しく動作するかを検証します。
  - `pytest`: Pythonのテストフレームワークで、テストの発見と実行をより柔軟に行うことができます。
- テスト:
  - `unittest`: Pythonの標準ライブラリに含まれるテストフレームワーク。
  - `pytest`: 高機能で拡張性の高いテストフレームワーク。
- ビルドツール:
  - 個別のビルドツールは使用されていません。Pythonスクリプトとして直接実行されます。
- 言語機能:
  - `Python 3.12+`: プロジェクトはPythonの最新機能と最適化を利用しています。
  - `TOML`: 設定ファイル形式として使用されており、人間が読み書きしやすいシンプルな構造を提供します。
  - `正規表現 (regex)`: ウィンドウタイトルをパターンマッチングするために利用されます。
- 自動化・CI/CD:
  - `pre-commit`: コードがリポジトリにコミットされる前に、自動的にリンティングやフォーマットを行うことで、コード品質を確保します。
- 開発標準:
  - `.editorconfig`: 異なるエディタやIDE間で一貫したコーディングスタイル（インデント、文字コードなど）を維持するための設定ファイルです。
  - `ruff`: コードのフォーマットとリンティングにより、一貫したコードスタイルと品質を強制します。

## ファイル階層ツリー
```
.editorconfig
.gitignore
.pre-commit-config.yaml
.vscode/
  settings.json
LICENSE
README.ja.md
README.md
_config.yml
config.toml.example
examples/
  example.txt
generated-docs/
issue-notes/
  11.md
  12.md
  13.md
  14.md
  15.md
  16.md
  21.md
  26.md
  27.md
  29.md
  31.md
  33.md
  34.md
  37.md
  39.md
  4.md
  40.md
  43.md
  45.md
  46.md
  48.md
  50.md
  6.md
  8.md
  9.md
pytest.ini
ruff.toml
src/
  __init__.py
  __main__.py
  config.py
  constants.py
  gui.py
  main.py
  score_tracker.py
  window_monitor.py
tests/
  test_config.py
  test_dummy.py
  test_gui.py
  test_score_colors.py
  test_score_tracker.py
  test_window_monitor.py
```

## ファイル詳細説明
- **.editorconfig**: 異なる開発環境（エディタやIDE）間でインデントスタイル、文字コードなどの基本的なコーディングスタイルを統一するための設定ファイルです。
- **.gitignore**: Gitのバージョン管理から除外するファイルやディレクトリを指定するファイルです（例: コンパイルされたファイル、一時ファイル、ユーザー固有の設定ファイルなど）。
- **.pre-commit-config.yaml**: `pre-commit`ツールがコミット前に実行するフック（コードフォーマット、リンティングなど）の設定を定義するファイルです。
- **.vscode/settings.json**: Visual Studio Codeエディタのワークスペース固有の設定を定義するファイルです。
- **LICENSE**: 本プロジェクトのソフトウェアライセンス情報が記載されています。
- **README.ja.md**: プロジェクトの目的、機能、インストール方法、使用法、設定方法など、日本語での詳細な説明を提供します。
- **README.md**: プロジェクトの目的、機能、インストール方法、使用法、設定方法など、英語での詳細な説明を提供します。
- **_config.yml**: GitHub Pagesなどの静的サイトジェネレーターで利用される可能性のある設定ファイルですが、本プロジェクトでの直接的な利用は不明です。
- **config.toml.example**: ユーザーがカスタマイズできる設定ファイル（`config.toml`）の例を提供します。ウィンドウパターンやスコア設定などが記述されています。
- **examples/example.txt**: プロジェクトに関連する使用例やデータサンプルが格納されるディレクトリ、またはファイルです。
- **generated-docs/**: 自動生成されたドキュメントやレポートが格納される予定のディレクトリです。
- **issue-notes/**: 開発中に発生した課題や検討事項に関するメモが保存されているディレクトリです。
- **pytest.ini**: `pytest`テストフレームワークの動作設定を定義するファイルです。
- **ruff.toml**: Pythonのリンターおよびフォーマッターである`ruff`の設定を定義するファイルです。
- **src/__init__.py**: `src`ディレクトリがPythonパッケージであることを示します。
- **src/__main__.py**: `python -m src`のようにモジュールとして実行された際のエントリポイントとなるファイルです。`main.py`の処理を呼び出します。
- **src/config.py**: TOML形式の設定ファイル（`config.toml`）を読み込み、アプリケーションが利用する設定値を管理するモジュールです。
- **src/constants.py**: アプリケーション全体で使用される固定値（定数）を定義するモジュールです。
- **src/gui.py**: `tkinter`ライブラリを使用して、スコア表示やステータス表示を行うユーザーインターフェースを構築・管理するモジュールです。
- **src/main.py**: アプリケーションの主要なエントリポイントであり、設定の読み込み、GUIの初期化、ウィンドウ監視ループのオーケストレーションを行います。
- **src/score_tracker.py**: アクティブなウィンドウタイトルに基づいてスコアを計算・追跡し、設定されたパターンとのマッチングロジックを管理するモジュールです。
- **src/window_monitor.py**: OSに依存しない形で、現在アクティブなウィンドウのタイトルを取得する機能を提供するモジュールです。
- **tests/test_config.py**: `src/config.py`モジュールの機能に関する単体テストを記述したファイルです。
- **tests/test_dummy.py**: テスト環境の設定や動作確認のためのダミー、または初期テストケースを記述したファイルです。
- **tests/test_gui.py**: `src/gui.py`モジュールのGUIコンポーネントに関する単体テストを記述したファイルです。
- **tests/test_score_colors.py**: スコアの変化に応じたGUIの色の表示ロジックに関する単体テストを記述したファイルです。
- **tests/test_score_tracker.py**: `src/score_tracker.py`モジュールのスコア計算・追跡ロジックに関する単体テストを記述したファイルです。
- **tests/test_window_monitor.py**: `src/window_monitor.py`モジュールのウィンドウタイトル取得機能に関する単体テストを記述したファイルです。

## 関数詳細説明
このプロジェクトでは、主に以下の関数やクラスのメソッドが重要な役割を担っています。

-   **`main.py`**
    *   `main()`: アプリケーションのメインエントリポイント。設定の読み込み、GUIの初期化、ウィンドウ監視とスコア更新のメインループを開始します。引数: なし。戻り値: なし。
    *   `parse_arguments()`: コマンドライン引数をパースし、カスタム設定ファイルのパスなどを処理します。引数: なし。戻り値: `argparse.Namespace`オブジェクト。
    *   `run_app()`: アプリケーションの主要なロジックをオーケストレーションし、GUIと監視ループを統合して実行します。引数: なし。戻り値: なし。

-   **`config.py`**
    *   `ConfigManager`クラス: 設定ファイルの読み込み、管理、およびデフォルト値の適用を行うクラス。
        *   `__init__(config_path)`: コンフィグマネージャーを初期化し、指定されたパスから設定ファイルを読み込みます。引数: `config_path` (str, 設定ファイルのパス)。戻り値: なし。
        *   `get_config()`: 現在の設定値を含む辞書形式のオブジェクトを返します。引数: なし。戻り値: dict。

-   **`window_monitor.py`**
    *   `get_active_window_title()`: 現在アクティブなウィンドウのタイトルをクロスプラットフォームで取得します。引数: なし。戻り値: str (ウィンドウタイトル) または None。

-   **`score_tracker.py`**
    *   `ScoreTracker`クラス: ウィンドウパターンとスコアを管理し、現在のスコアを追跡するクラス。
        *   `__init__(config)`: `ScoreTracker`を初期化し、設定（ウィンドウパターン、デフォルトスコアなど）をロードします。引数: `config` (dict, 設定オブジェクト)。戻り値: なし。
        *   `update_score(window_title)`: 指定されたウィンドウタイトルに基づいてスコアを計算し、更新します。引数: `window_title` (str, アクティブなウィンドウタイトル)。戻り値: int (スコアの増減量)。
        *   `get_current_score()`: 現在の合計スコアを返します。引数: なし。戻り値: int。
        *   `get_last_matched_description()`: 最後にマッチしたウィンドウパターンの説明を返します。引数: なし。戻り値: str。
        *   `reset_score()`: 現在のスコアを0にリセットします。引数: なし。戻り値: なし。
        *   `is_score_decreasing()`: 現在のスコアが直前の更新で減少したかどうかを判定します。引数: なし。戻り値: bool。

-   **`gui.py`**
    *   `CatWindowWatcherGUI`クラス: tkinterベースのGUIを構築し、スコアとステータスを表示するクラス。
        *   `__init__(master, config, score_tracker, get_window_title_func)`: GUIを初期化し、スコアトラッカーやウィンドウタイトル取得関数と連携させます。引数: `master` (tkinter.Tk), `config` (dict), `score_tracker` (ScoreTracker), `get_window_title_func` (callable)。戻り値: なし。
        *   `update_display()`: スコアとステータス表示を更新します。定期的に呼び出され、GUIの状態を最新にします。引数: なし。戻り値: なし。
        *   `start()`: GUIのメインループを開始し、イベント処理を開始します。引数: なし。戻り値: なし。
        *   `apply_transparency(transparency)`: ウィンドウの透明度を設定します。引数: `transparency` (float)。戻り値: なし。
        *   `toggle_always_on_top(always_on_top)`: ウィンドウの最前面表示を切り替えます。引数: `always_on_top` (bool)。戻り値: なし。
        *   `handle_mouse_proximity()`: マウスカーソルの接近に応じてウィンドウの最前面表示を自動で切り替える機能（邪魔にならないように）。引数: なし。戻り値: なし。
        *   `check_for_score_decrease()`: スコア減少時に特定の視覚効果（例: ウィンドウを最前面に固定）を適用するかどうかを判断し実行します。引数: なし。戻り値: なし。
        *   `fade_window_for_flow_mode()`: フローモードが有効な場合、時間の経過とともにウィンドウを徐々に透明化する処理を管理します。引数: なし。戻り値: なし。

## 関数呼び出し階層ツリー
```
main.py
  ├── parse_arguments()
  └── run_app()
        ├── config.py::ConfigManager (設定を読み込み、管理するインスタンスを生成)
        │     └── ConfigManager.__init__(config_path)
        │           └── ConfigManager.get_config() (設定値を取得)
        ├── score_tracker.py::ScoreTracker (スコアを追跡、更新するインスタンスを生成)
        │     └── ScoreTracker.__init__(config)
        ├── window_monitor.py::get_active_window_title() (現在のアクティブウィンドウタイトルを取得)
        └── gui.py::CatWindowWatcherGUI (ユーザーインターフェースを表示、管理するインスタンスを生成)
              ├── CatWindowWatcherGUI.__init__(master, config, score_tracker, get_window_title_func)
              ├── CatWindowWatcherGUI.start() (GUIのメインループを開始)
              └── (定期実行ループ - 例: 1秒ごと)
                    ├── window_monitor.get_active_window_title()
                    ├── score_tracker.update_score(window_title)
                    │     ├── score_tracker.get_current_score()
                    │     └── score_tracker.get_last_matched_description()
                    ├── gui.update_display()
                    │     ├── gui.apply_transparency(transparency)
                    │     ├── gui.toggle_always_on_top(always_on_top)
                    │     ├── gui.handle_mouse_proximity()
                    │     ├── gui.check_for_score_decrease()
                    │     └── gui.fade_window_for_flow_mode()
                    └── (スコアのリセット処理や特定の時間に基づく更新ロジック)
                          └── score_tracker.reset_score()
```
*このツリーは提供された情報と一般的なアプリケーション構造から推測される主要な呼び出し関係を示しています。実際の詳細な呼び出しはコードに依存します。*

---
Generated at: 2026-01-06 07:06:28 JST
