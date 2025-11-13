Last updated: 2025-11-14

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、生産性に基づいてスコアを調整するシンプルなツールです。
- GitHubでの作業中にスコアを上げ、SNS閲覧時にスコアを下げるなど、カスタマイズ可能です。
- 「猫が見守る」というコンセプトで、現在の活動を視覚的に表示します。

## 技術スタック
- フロントエンド: **tkinter** (Pythonの標準GUIライブラリで、シンプルでクリーンなユーザーインターフェースを提供します。)
- 音楽・オーディオ: (このプロジェクトには音楽・オーディオ関連の技術は使用されていません。)
- 開発ツール: **Git** (バージョン管理システムとしてソースコードの管理に使用)、**.editorconfig** (異なるエディタ間でのコーディングスタイル統一を支援)、**.vscode/settings.json** (VS Codeのワークスペース固有の設定)、**pre-commit** (コミット前に自動でコード品質チェックやフォーマットを実行するフック管理ツール)。
- テスト: **unittest** (Python標準のテストフレームワークで、コードの機能テストに使用されます。)
- ビルドツール: (Pythonスクリプトとして直接実行されるため、特定のビルドツールは使用されていません。Python 3.12以上が実行環境として必要です。)
- 言語機能: **Python 3.12以上** (プロジェクトの主要開発言語)、**正規表現 (regex)** (ウィンドウタイトルパターンマッチングに利用されます)。
- 自動化・CI/CD: **pre-commit** (コードコミット前の自動チェックに利用され、品質保持と開発プロセスの自動化に貢献します)。
- 開発標準: **ruff** (Pythonの高速なリンターおよびフォーマッターで、コード品質の維持と統一されたコーディングスタイルの適用に使用されます。)

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
  4.md
pytest.ini
ruff.toml
src/
  __init__.py
  __main__.py
  config.py
  gui.py
  main.py
  score_tracker.py
  window_monitor.py
tests/
  test_config.py
  test_dummy.py
  test_score_tracker.py
  test_window_monitor.py
```

## ファイル詳細説明
-   `.editorconfig`: さまざまなエディタやIDEで一貫したコーディングスタイルを定義するための設定ファイルです。
-   `.gitignore`: Gitがバージョン管理の対象から外すファイルやディレクトリを指定するファイルです。
-   `.pre-commit-config.yaml`: `pre-commit`ツールで使用される設定ファイルで、コミット前に実行されるフック（コードフォーマット、リンティングなど）を定義します。
-   `.vscode/settings.json`: Visual Studio Codeエディタのワークスペース固有の設定を定義するファイルです。
-   `LICENSE`: プロジェクトのソフトウェアライセンス情報が記載されています。
-   `README.ja.md`, `README.md`: プロジェクトの概要、インストール方法、使用方法、機能などを説明する日本語版および英語版のドキュメントです。
-   `_config.yml`: 一般的にGitHub Pagesなどの静的サイトジェネレータの設定に使用されるファイルですが、このプロジェクトでの具体的な用途は不明です。
-   `config.toml.example`: アプリケーションの設定ファイル（`config.toml`）の記述例を提供します。ウィンドウパターンやスコア設定のカスタマイズ方法が示されています。
-   `examples/example.txt`: プロジェクトの機能や使用例を示すためのサンプルファイルです。
-   `generated-docs/`: ドキュメント生成ツールによって作成されたドキュメントを格納するためのディレクトリです。
-   `issue-notes/4.md`: 特定のIssue（問題報告や機能要望）に関するメモや詳細情報を記録するためのファイルです。
-   `pytest.ini`: Pythonのテストフレームワークである`pytest`の設定ファイルです。ただし、プロジェクトでは`unittest`が主に利用されています。
-   `ruff.toml`: コードリンターおよびフォーマッターである`ruff`の設定ファイルで、コードの品質基準やフォーマットルールを定義します。
-   `src/__init__.py`: `src`ディレクトリがPythonパッケージであることを示すファイルです。
-   `src/__main__.py`: `python -m src`のようにモジュールとして実行された際のエントリポイントとなるファイルで、通常は`main.py`の関数を呼び出します。
-   `src/config.py`: TOML形式の設定ファイルを読み込み、アプリケーション内で利用可能な形式に変換する役割を担います。
-   `src/gui.py`: `tkinter`ライブラリを使用して、スコア表示などのユーザーインターフェースを構築・管理します。
-   `src/main.py`: アプリケーションの主要なエントリポイントです。設定の読み込み、GUIの初期化、ウィンドウ監視ループの開始など、全体の処理フローをオーケストレーションします。
-   `src/score_tracker.py`: アクティブなウィンドウタイトルを設定されたパターンと照合し、それに基づいてスコアを計算・更新するビジネスロジックを実装します。
-   `src/window_monitor.py`: OSに依存しない形で、現在アクティブなウィンドウのタイトルを取得する機能を提供します。
-   `tests/test_config.py`: `src/config.py`モジュールのテストコードを含みます。
-   `tests/test_dummy.py`: テストフレームワークの動作確認や一時的なテストに使用されるダミーのテストファイルです。
-   `tests/test_score_tracker.py`: `src/score_tracker.py`モジュールのテストコードを含みます。
-   `tests/test_window_monitor.py`: `src/window_monitor.py`モジュールのテストコードを含みます。

## 関数詳細説明
-   `src/config.py`:
    -   `load_config(file_path: str) -> dict`: 指定されたTOMLファイルパスから設定を読み込み、辞書形式で返します。
        -   引数: `file_path` (str): 設定ファイルのパス。
        -   戻り値: `dict`: 読み込まれた設定データ。
    -   `get_window_patterns(config_data: dict) -> list[dict]`: 読み込まれた設定データから、ウィンドウ監視パターン（正規表現、スコア、説明）のリストを抽出して返します。
        -   引数: `config_data` (dict): `load_config`で読み込まれた設定データ。
        -   戻り値: `list[dict]`: ウィンドウパターンのリスト。
-   `src/window_monitor.py`:
    -   `get_active_window_title() -> str`: 現在アクティブなウィンドウのタイトルをOS固有のAPIを使用して取得し、文字列で返します。
        -   引数: なし。
        -   戻り値: `str`: アクティブなウィンドウのタイトル。
-   `src/score_tracker.py`:
    -   `ScoreTracker` クラス: ウィンドウパターンに基づいてスコアを追跡・管理します。
        -   `__init__(patterns: list[dict])`: `ScoreTracker`オブジェクトを初期化します。監視するウィンドウパターンリストを受け取ります。
            -   引数: `patterns` (list[dict]): `get_window_patterns`で取得したパターンリスト。
        -   `update_score(window_title: str) -> None`: 指定されたウィンドウタイトルとパターンを比較し、マッチした場合にスコアを更新します。
            -   引数: `window_title` (str): 現在アクティブなウィンドウのタイトル。
        -   `get_current_score() -> int`: 現在の累積スコアを返します。
            -   引数: なし。
            -   戻り値: `int`: 現在のスコア。
        -   `get_last_matched_description() -> str`: 最後にマッチしたウィンドウパターンの説明文を返します。
            -   引数: なし。
            -   戻り値: `str`: 最後にマッチしたパターンの説明。
-   `src/gui.py`:
    -   `create_gui(initial_score: int, update_callback: callable) -> tkinter.Tk`: GUIウィンドウを作成し、初期スコアを設定し、更新コールバックを登録します。
        -   引数: `initial_score` (int): 初期表示スコア。`update_callback` (callable): 定期的にGUIを更新するための関数。
        -   戻り値: `tkinter.Tk`: 生成されたTkinterルートウィンドウオブジェクト。
    -   `update_display(root: tkinter.Tk, score_var: tkinter.IntVar, desc_var: tkinter.StringVar, score: int, description: str) -> None`: GUI上のスコアと説明表示を更新します。
        -   引数: `root` (tkinter.Tk), `score_var` (tkinter.IntVar), `desc_var` (tkinter.StringVar): GUI要素への参照。 `score` (int): 新しいスコア。 `description` (str): 新しい説明。
-   `src/main.py`:
    -   `main()`: アプリケーションのメイン実行関数です。設定の読み込み、`ScoreTracker`とGUIの初期化、そしてメインの監視ループ（`run_watcher`）を開始します。
        -   引数: なし。
        -   戻り値: なし。
    -   `run_watcher(root: tkinter.Tk, score_tracker: ScoreTracker, score_var: tkinter.IntVar, desc_var: tkinter.StringVar, interval: int = 1000) -> None`: 一定間隔でアクティブなウィンドウを監視し、スコアを更新し、GUIを最新の状態に保つループを実行します。
        -   引数: `root` (tkinter.Tk): GUIのルートウィンドウ。 `score_tracker` (ScoreTracker): スコア追跡オブジェクト。 `score_var` (tkinter.IntVar): GUIのスコア表示変数。 `desc_var` (tkinter.StringVar): GUIの説明表示変数。 `interval` (int): 監視間隔（ミリ秒）。

## 関数呼び出し階層ツリー
```
プロジェクト情報より、関数呼び出し階層の分析は提供されていません。
しかし、一般的なアプリケーションのフローから以下の呼び出し関係が推測されます。

main.py::main()
├── config.py::load_config()
├── config.py::get_window_patterns()
├── score_tracker.py::ScoreTracker.__init__()
├── gui.py::create_gui()
│   └── gui.py::update_display() (初期表示)
└── main.py::run_watcher() (メインループ)
    ├── window_monitor.py::get_active_window_title()
    ├── score_tracker.py::ScoreTracker.update_score()
    ├── score_tracker.py::ScoreTracker.get_current_score()
    ├── score_tracker.py::ScoreTracker.get_last_matched_description()
    └── gui.py::update_display()

---
Generated at: 2025-11-14 07:06:29 JST
