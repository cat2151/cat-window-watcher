Last updated: 2026-02-02

# Project Overview

## プロジェクト概要
- ユーザーのアクティブなウィンドウを監視し、作業内容に応じてリアルタイムでスコアを増減させるツールです。
- 生産的な活動に報奨を与え、非生産的な活動を抑制するように設定することで、集中力の向上をサポートします。
- シンプルなGUI、正規表現ベースの柔軟な設定、クロスプラットフォーム対応を特徴とする軽量なアプリケーションです。

## 技術スタック
- フロントエンド: Tkinter (Pythonの標準GUIライブラリで、シンプルかつ軽量なユーザーインターフェースを提供), AppleScript (macOSでウィンドウ情報を取得するために利用), Windows API (Windowsでウィンドウ情報を取得するために利用)
- 音楽・オーディオ: 該当なし
- 開発ツール: Git (バージョン管理システム), Ruff (Pythonコードのフォーマットとリンティングツール), EditorConfig (異なるIDEやエディタ間でのコードスタイル統一), Pre-commit (コミット前に自動でコードチェックを行うフック管理ツール), VS Code (開発環境の推奨設定)
- テスト: unittest (Python標準のユニットテストフレームワーク), pytest (高度なテスト機能とシンプルな記述を提供するPythonテストフレームワーク)
- ビルドツール: TOML (設定ファイルを記述するためのシンプルで読みやすいマークアップ言語)
- 言語機能: Python 3.12+ (プロジェクトの主要なプログラミング言語)
- 自動化・CI/CD: Pre-commit (コミット前の自動化チェック)
- 開発標準: Ruff (コードフォーマットとリンティングによるコード品質の維持)

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
  📖 README.ja.md
  📖 README.md
  📄 example1_productivity.ja.toml
  📄 example1_productivity.toml
  📄 example2_study_time.ja.toml
  📄 example2_study_time.toml
  📄 example3_always_on_top.ja.toml
  📄 example3_always_on_top.toml
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
  📖 45.md
  📖 46.md
  📖 48.md
  📖 50.md
  📖 53.md
  📖 55.md
  📖 57.md
  📖 58.md
  📖 59.md
  📖 6.md
  📖 60.md
  📖 61.md
  📖 63.md
  📖 65.md
  📖 73.md
  📖 75.md
  📖 77.md
  📖 8.md
  📖 9.md
📄 pytest.ini
📄 ruff.toml
📁 src/
  📄 __init__.py
  📄 __main__.py
  📄 config.py
  📄 config_loader.py
  📄 config_validator.py
  📄 constants.py
  📄 flow_state_manager.py
  📄 gui.py
  📄 main.py
  📄 score_calculator.py
  📄 score_tracker.py
  📄 status_formatter.py
  📄 window_behavior.py
  📄 window_monitor.py
📁 tests/
  📄 test_config.py
  📄 test_dummy.py
  📄 test_gui.py
  📄 test_score_colors.py
  📄 test_score_tracker.py
  📄 test_screensaver_detection.py
  📄 test_window_monitor.py
```

## ファイル詳細説明
- **`.editorconfig`**: 異なるIDEやエディタ間で、インデントスタイル、文字コードなどのコーディングスタイルを統一するための設定ファイルです。
- **`.gitignore`**: Gitがバージョン管理の対象としないファイルやディレクトリ（例: ビルド生成物、ログファイル）を指定するファイルです。
- **`.pre-commit-config.yaml`**: Gitコミット前に自動的に実行されるフック（コードフォーマットやリンティングなど）を設定するためのファイルです。
- **`.vscode/settings.json`**: Visual Studio Codeエディタにおけるプロジェクト固有の設定を定義します。
- **`LICENSE`**: プロジェクトのソフトウェアライセンス情報が記載されています。
- **`README.ja.md`, `README.md`**: プロジェクトの目的、機能、インストール方法、使用方法などを説明するドキュメント（日本語版と英語版）。
- **`_config.yml`**: GitHub Pagesなどの静的サイトジェネレータでドキュメントサイトを構築する際の設定ファイルとして使用されることがあります。
- **`config.toml.example`**: ユーザーがアプリケーションの設定を行うためのテンプレートファイルです。これをコピーして`config.toml`を作成し編集します。
- **`examples/`**: さまざまな使用シナリオに対応する設定例のファイル群を格納しているディレクトリです。
    - **`examples/README.ja.md`, `examples/README.md`**: `examples`ディレクトリの内容を説明するドキュメント。
    - **`examples/example*.toml`**: 生産性追跡、勉強時間、ウィンドウの挙動設定などの具体的な設定例ファイル。
- **`pytest.ini`**: Pythonのテストフレームワークであるpytestの設定ファイルです。テストの実行方法やオプションを定義します。
- **`ruff.toml`**: Pythonコードのフォーマットとリンティングを行うRuffツールの設定ファイルです。コード品質と一貫性を保ちます。
- **`src/__init__.py`**: `src`ディレクトリがPythonパッケージであることを示すファイルです。
- **`src/__main__.py`**: `python -m src`のようにモジュールとして実行された際のエントリポイントとなるファイルです。
- **`src/config.py`**: アプリケーションのグローバル設定値を保持し、アクセスするためのモジュールです。
- **`src/config_loader.py`**: TOML形式の設定ファイル（`config.toml`）を読み込み、解析するロジックをカプセル化したモジュールです。
- **`src/config_validator.py`**: 読み込まれた設定値が有効な形式であり、アプリケーションが正しく動作するための要件を満たしているかを検証するモジュールです。
- **`src/constants.py`**: アプリケーション全体で使用される固定値や定数を一元的に定義するモジュールです。
- **`src/flow_state_manager.py`**: ユーザーの集中状態（フロー状態）を管理し、それに応じてウィンドウの透明度を変化させるなどの挙動を制御するモジュールです。
- **`src/gui.py`**: PythonのTkinterライブラリを使用して、スコア表示やステータス表示などのユーザーインターフェースを構築・管理するモジュールです。
- **`src/main.py`**: アプリケーションの主要なエントリポイントであり、設定の読み込み、GUIの初期化、メインの監視ループのオーケストレーションを行います。
- **`src/score_calculator.py`**: 現在のアクティブウィンドウタイトルと設定されたパターンに基づいて、スコアの増減値を計算するロジックを含むモジュールです。
- **`src/score_tracker.py`**: アプリケーションの現在のスコア値を追跡し、スコアのリセットやデフォルトスコアの適用など、スコアに関連する状態管理を行うモジュールです。
- **`src/status_formatter.py`**: GUIに表示される、現在マッチしているウィンドウ情報やスコア変動に関するステータス文字列を整形するモジュールです。
- **`src/window_behavior.py`**: アプリケーションのGUIウィンドウが持つ動的な挙動（常に最前面表示、マウス接近時の移動、透明度変更など）を実装・管理するモジュールです。
- **`src/window_monitor.py`**: 現在アクティブなウィンドウのタイトルを、オペレーティングシステム（Linux, macOS, Windows）に依存しない方法で取得する機能を提供するモジュールです。
- **`tests/`**: アプリケーションの各コンポーネントの機能と正確性を検証するためのテストコードを格納するディレクトリです。
    - **`tests/test_config.py`**: 設定関連モジュールの単体テスト。
    - **`tests/test_dummy.py`**: 初期設定や簡単なテストに使用されるダミーのテストファイル。
    - **`tests/test_gui.py`**: GUIモジュールの機能に関するテスト。
    - **`tests/test_score_colors.py`**: スコアの増減による表示色の変化を検証するテスト。
    - **`tests/test_score_tracker.py`**: スコア追跡ロジックの正確性を検証するテスト。
    - **`tests/test_screensaver_detection.py`**: スクリーンセーバーがアクティブな場合の挙動をテスト（実装されている場合）。
    - **`tests/test_window_monitor.py`**: ウィンドウ監視機能のテスト。

## 関数詳細説明
- **`main.main()`**:
    - 役割: アプリケーションの起動と主要な処理フローを管理するエントリポイント。
    - 機能: 設定ファイルの読み込み、GUIの初期化、定期的なウィンドウ監視とスコア更新のループを開始します。
- **`config_loader.load_config(config_path: str)`**:
    - 役割: 指定されたパスからTOML形式の設定ファイルを読み込む。
    - 引数: `config_path` (str) - 設定ファイルのパス。
    - 戻り値: 読み込んだ設定データを含む辞書。
    - 機能: ファイルが存在しない場合や解析エラーが発生した場合のハンドリングも行います。
- **`config_validator.validate_config(config_data: dict)`**:
    - 役割: 読み込まれた設定データがアプリケーションの期待する形式と要件を満たしているかを検証する。
    - 引数: `config_data` (dict) - 読み込まれた設定データ。
    - 戻り値: 検証済みの設定データ（必要に応じてデフォルト値が適用される場合あり）。
    - 機能: 不正な設定値や不足している必須項目を特定し、適切なエラーまたは警告を発します。
- **`window_monitor.get_active_window_title()`**:
    - 役割: 現在フォーカスされているアクティブなウィンドウのタイトルを取得する。
    - 引数: なし。
    - 戻り値: アクティブなウィンドウのタイトル (str)。取得できない場合は空文字列。
    - 機能: Linux, macOS, Windowsそれぞれで適切なOSネイティブAPIやツールを使用してウィンドウタイトルをクロスプラットフォームで取得します。
- **`score_tracker.update_score(window_title: str)`**:
    - 役割: 現在のアクティブウィンドウタイトルに基づいてスコアを更新する。
    - 引数: `window_title` (str) - 現在アクティブなウィンドウのタイトル。
    - 戻り値: スコアの変化量 (int) と、マッチしたパターンの説明 (str)。
    - 機能: 内部で`score_calculator`を呼び出し、スコアを計算し、現在のスコアを管理・更新します。設定されたリセットロジックなども適用します。
- **`score_tracker.get_current_score()`**:
    - 役割: 現在のスコア値を取得する。
    - 引数: なし。
    - 戻り値: 現在のスコア (int)。
    - 機能: `score_tracker`が保持する最新のスコアを返します。
- **`score_calculator.calculate_score_change(window_title: str, config: dict, current_score: int, self_window_title: str)`**:
    - 役割: 指定されたウィンドウタイトルと設定に基づいて、スコアの増減量を計算する。
    - 引数: `window_title` (str), `config` (dict), `current_score` (int), `self_window_title` (str)。
    - 戻り値: 計算されたスコアの変化量 (int) と、マッチしたパターンの説明 (str)。
    - 機能: 正規表現マッチング、デフォルトスコア適用モード、マイルドペナルティモード、自己ウィンドウスコアなど、複雑なスコア計算ロジックを処理します。
- **`gui.init_gui(root: tk.Tk, score_tracker, config: dict, window_behavior_manager)`**:
    - 役割: TkinterのメインウィンドウとUI要素を初期化する。
    - 引数: `root` (tk.Tk), `score_tracker`, `config` (dict), `window_behavior_manager`。
    - 戻り値: なし。
    - 機能: スコア表示ラベル、ステータス表示ラベルなどを配置し、ウィンドウの初期設定（位置、透明度など）を適用します。
- **`gui.update_gui()`**:
    - 役割: 定期的にGUIを更新し、最新のスコアとステータスを表示する。
    - 引数: なし。
    - 戻り値: なし。
    - 機能: `score_tracker`から最新のスコアを取得し、`status_formatter`で整形されたメッセージと共にGUIに反映させます。フロー状態に応じたウィンドウのフェード処理などもトリガーします。
- **`window_behavior.apply_always_on_top(window: tk.Tk, config: dict)`**:
    - 役割: ウィンドウの「常に最前面表示」設定を適用または解除する。
    - 引数: `window` (tk.Tk), `config` (dict)。
    - 戻り値: なし。
    - 機能: `config`で設定された`always_on_top`や`always_on_top_while_score_decreasing`に基づいて、ウィンドウの最前面表示を制御します。
- **`window_behavior.handle_mouse_proximity(window: tk.Tk, config: dict)`**:
    - 役割: マウスカーソルがウィンドウに近づいたときに、ウィンドウを最背面または最前面に移動させる挙動を管理する。
    - 引数: `window` (tk.Tk), `config` (dict)。
    - 戻り値: なし。
    - 機能: `hide_on_mouse_proximity`が有効な場合に、マウスとウィンドウの距離を監視し、ウィンドウのZオーダーを調整します。
- **`window_behavior.set_window_transparency(window: tk.Tk, alpha: float)`**:
    - 役割: ウィンドウの透明度を設定する。
    - 引数: `window` (tk.Tk), `alpha` (float) - 透明度 (0.0=完全に透明, 1.0=完全に不透明)。
    - 戻り値: なし。
    - 機能: OSの機能を利用してウィンドウの不透明度を変更します。
- **`flow_state_manager.update_flow_state(score_change: int)`**:
    - 役割: スコアの変化に基づいてユーザーのフロー状態（集中状態）を更新し、関連する挙動（ウィンドウのフェードなど）を制御する。
    - 引数: `score_change` (int) - 前回のスコア変化量。
    - 戻り値: なし。
    - 機能: スコアが継続的に上昇している場合にフロー状態とみなし、ウィンドウの透明化を開始・進行させます。
- **`status_formatter.format_status_message(last_matched_description: str, last_window_title: str, last_score_change: int)`**:
    - 役割: GUIに表示するステータス文字列を整形する。
    - 引数: `last_matched_description` (str), `last_window_title` (str), `last_score_change` (int)。
    - 戻り値: 整形されたステータス文字列 (str)。
    - 機能: マッチしたパターンの説明、ウィンドウタイトル、スコアの変化量などを用いて、ユーザーに分かりやすいメッセージを作成します。

## 関数呼び出し階層ツリー
```
main.py
└── main()
    ├── config_loader.load_config()
    ├── config_validator.validate_config()
    ├── gui.init_gui()
    │   └── gui.update_gui() (定期的に呼び出される)
    │       ├── window_monitor.get_active_window_title()
    │       ├── score_tracker.update_score()
    │       │   └── score_calculator.calculate_score_change()
    │       ├── status_formatter.format_status_message()
    │       ├── flow_state_manager.update_flow_state()
    │       ├── window_behavior.apply_always_on_top()
    │       ├── window_behavior.handle_mouse_proximity()
    │       └── window_behavior.set_window_transparency()
    └── score_tracker.get_current_score()

---
Generated at: 2026-02-02 07:06:38 JST
