Last updated: 2026-02-06

# Project Overview

## プロジェクト概要
- ユーザーのアクティブなウィンドウを監視し、作業内容に基づいて生産性スコアを調整するツールです。
- GitHubでの作業でスコアが上がり、SNS閲覧で下がるなど、正規表現で定義可能なルールで動作します。
- シンプルなTkinter GUIでスコアと現在の活動を表示し、クロスプラットフォームで動作する軽量なアプリケーションです。

## 技術スタック
- フロントエンド: **Python Tkinter** (Pythonの標準GUIライブラリで、シンプルでクリーンなユーザーインターフェースを提供します)
- 音楽・オーディオ: (該当する技術はありません)
- 開発ツール:
    - **Git**: ソースコードのバージョン管理に使用。
    - **ruff**: Pythonコードの高速なフォーマッターおよびリンターとして、コード品質と一貫性を保ちます。
    - **unittest**: Python標準のテストフレームワークで、各種モジュールの単体テストを実行します。
    - **pytest**: Pythonのテストフレームワークで、柔軟なテストの記述と実行を可能にします。
    - **TOML**: アプリケーションの設定ファイル形式として採用されており、人間が読みやすく、扱いやすい構造を提供します。
    - **.editorconfig**: 複数の開発者やエディタ間でのコーディングスタイルの一貫性を保証します。
- テスト: **Python unittest**, **pytest** (上記「開発ツール」を参照)
- ビルドツール: **Pythonスクリプト実行** (Pythonインタプリタにより直接スクリプトが実行されます)
- 言語機能: **Python 3.12以上** (アプリケーションの基盤となるプログラミング言語バージョン)
    - **プラットフォーム連携**:
        - **xdotool / xprop**: Linux環境でアクティブウィンドウ情報を取得するために使用されます。
        - **AppleScript**: macOS環境でアクティブウィンドウ情報を取得するために組み込みで利用されます。
        - **pywin32 (オプション)**: Windows環境でより強力なウィンドウ操作と互換性を提供するために利用されるPython拡張です。
- 自動化・CI/CD: **pre-commit**: コミット前にコードのフォーマットやリンティングを自動的に実行し、品質基準を維持します。
- 開発標準: **ruff**, **.editorconfig** (上記「開発ツール」を参照)

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
📁 docs/
  📖 game-detection-guide.md
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
  📖 78.md
  📖 8.md
  📖 80.md
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
  📄 test_game_detection.py
  📄 test_gui.py
  📄 test_score_colors.py
  📄 test_score_tracker.py
  📄 test_screensaver_detection.py
  📄 test_window_monitor.py
```

## ファイル詳細説明
- **.editorconfig**: エディタのコードスタイル設定を定義し、プロジェクト全体のコードの一貫性を維持します。
- **.gitignore**: Gitがバージョン管理の対象外とするファイルやディレクトリを指定します。
- **.pre-commit-config.yaml**: コミット前に自動的に実行されるフック（例: コード整形、リンティング）の設定を定義します。
- **.vscode/settings.json**: Visual Studio Codeのワークスペース固有の設定を格納し、開発環境を統一します。
- **LICENSE**: プロジェクトのライセンス情報が記述されたファイルです。
- **README.ja.md, README.md**: プロジェクトの目的、機能、使用方法、設定例などを日本語と英語で説明するメインドキュメントです。
- **_config.yml**: GitHub Pagesなどの静的サイトジェネレータの設定ファイルである可能性があります。
- **config.toml.example**: アプリケーションの動作をカスタマイズするための設定ファイルのサンプルです。ウィンドウパターンやスコア調整、UI挙動などのオプションが含まれます。
- **docs/game-detection-guide.md**: ゲームアプリケーションの検知に関する特定のガイドラインや実装上の注意点などを説明するドキュメントです。
- **examples/**: 様々なユースケースに対応する設定ファイル（TOML形式）の具体例と、その説明（READMEファイル）が格納されています。
- **generated-docs/**: 自動生成されたドキュメントやレポートを格納するためのディレクトリです。
- **issue-notes/**: 開発中の課題や特定のIssueに関する詳細なメモ、調査結果、解決策などをまとめたドキュメント群です。
- **pytest.ini**: Pythonのテストフレームワークであるpytestの動作設定を定義するファイルです。
- **ruff.toml**: Pythonコードのリンターおよびフォーマッターであるruffの設定を定義するファイルです。
- **src/__init__.py**: `src`ディレクトリがPythonパッケージであることを示します。
- **src/__main__.py**: `python -m src`のようにモジュールとして実行された際のエントリポイントとなるファイルです。
- **src/config.py**: TOML形式の設定ファイルを読み込み、アプリケーション全体で利用可能な設定オブジェクトとして提供します。設定のデフォルト値適用や基本的なバリデーションも担当します。
- **src/config_loader.py**: `config.toml`ファイルから生の設定データを読み込む具体的なロジックを実装します。
- **src/config_validator.py**: 読み込まれた設定データの構造と値がアプリケーションの要件を満たしているかを検証します。
- **src/constants.py**: アプリケーション全体で共通して使用される定数（例: デフォルト値、マジックナンバーなど）を定義します。
- **src/flow_state_manager.py**: ユーザーの「フロー状態」（集中状態）を管理し、それに基づいてGUIウィンドウの透明度を制御するロジックを提供します。
- **src/gui.py**: PythonのTkinterライブラリを使用して、現在のスコアやアクティビティを表示するユーザーインターフェースを構築・管理します。
- **src/main.py**: アプリケーションのメインエントリポイントです。設定の読み込み、GUIの初期化、ウィンドウ監視とスコア更新のループ開始など、主要なコンポーネントの連携を調整します。
- **src/score_calculator.py**: アクティブなウィンドウタイトルと設定された正規表現パターンを比較し、それに基づいてスコアの増減量を計算する中心的なロジックを提供します。
- **src/score_tracker.py**: `window_monitor`から取得したウィンドウタイトルを`score_calculator`に渡し、全体のスコアをリアルタイムで追跡・更新します。スコアのリセットや履歴管理も行う可能性があります。
- **src/status_formatter.py**: 現在のスコアやマッチしたウィンドウパターン、スコアの変化量などを、GUIに表示するために整形されたテキスト形式に変換します。
- **src/window_behavior.py**: ウィンドウの最前面表示設定、マウス接近時の自動移動、スコア減少時の最前面化など、GUIウィンドウの動的な挙動を管理します。
- **src/window_monitor.py**: Linux、macOS、Windowsといった異なるオペレーティングシステムに対応した方法で、現在アクティブなウィンドウのタイトルを取得する役割を担います。
- **tests/**: プロジェクトの各モジュールや機能に対する単体テストコードを格納するディレクトリです。アプリケーションの品質と信頼性を保証するために使用されます。

## 関数詳細説明
- **main.py::main()**:
    - 役割: アプリケーションの起動エントリポイント。設定をロードし、GUIコンポーネントとスコア監視ループを初期化・開始します。
    - 引数: なし。コマンドライン引数で設定ファイルのパスを受け取ることがあります。
    - 戻り値: なし。
- **config.py::load_app_config(config_path=None)**:
    - 役割: 指定されたパスからTOML設定ファイルを読み込み、アプリケーション全体で使用される設定オブジェクトを生成します。デフォルト値の適用や読み込み後のバリデーションも行います。
    - 引数: `config_path` (str, optional): 設定ファイルのパス。指定がない場合はデフォルトパスを使用。
    - 戻り値: (dict): 読み込まれたアプリケーション設定。
- **gui.py::GUI.__init__(self, root, config, score_tracker, flow_state_manager, window_behavior)**:
    - 役割: Tkinter GUIウィンドウを初期化し、スコア表示ラベル、ステータス表示、ウィンドウのサイズと位置、色などの視覚要素を設定します。主要なロジックコンポーネントへの参照を持ちます。
    - 引数: `root` (tkinter.Tk), `config` (dict), `score_tracker` (ScoreTracker), `flow_state_manager` (FlowStateManager), `window_behavior` (WindowBehavior)。
    - 戻り値: なし。
- **gui.py::GUI.update_display(self)**:
    - 役割: 1秒ごとに実行され、`window_monitor`からウィンドウタイトルを取得し、`score_tracker`でスコアを更新し、`status_formatter`で整形されたテキストをGUIに表示します。`flow_state_manager`や`window_behavior`と連携してウィンドウの透明度や位置も調整します。
    - 引数: `self`。
    - 戻り値: なし。
- **gui.py::GUI.start_update_loop(self)**:
    - 役割: GUIの表示更新を定期的に（通常1秒ごと）開始するためのタイマーまたはスケジューラを設定します。
    - 引数: `self`。
    - 戻り値: なし。
- **window_monitor.py::get_active_window_title()**:
    - 役割: 現在アクティブな（フォーカスされている）ウィンドウのタイトル文字列を、OS固有のAPIやツール（Linuxの`xdotool`、macOSのAppleScript、Windows APIなど）を使用して取得します。
    - 引数: なし。
    - 戻り値: (str): アクティブウィンドウのタイトル。取得できなかった場合は空文字列。
- **score_tracker.py::ScoreTracker.__init__(self, config, score_calculator)**:
    - 役割: スコア追跡ロジックを初期化します。設定オブジェクトとスコア計算を担当する`score_calculator`への参照を保持します。
    - 引数: `config` (dict), `score_calculator` (ScoreCalculator)。
    - 戻り値: なし。
- **score_tracker.py::ScoreTracker.update_score(self, window_title)**:
    - 役割: 与えられたウィンドウタイトルを基に`score_calculator`を使ってスコアの変化量を決定し、現在の累積スコアを更新します。30分ごとのリセット機能なども管理します。
    - 引数: `window_title` (str): 現在アクティブなウィンドウのタイトル。
    - 戻り値: (int): 更新されたスコア。
- **score_tracker.py::ScoreTracker.get_current_status(self)**:
    - 役割: 現在のスコア値と、最後にマッチしたウィンドウパターンの説明（またはマッチしなかった旨のメッセージ）を返します。
    - 引数: `self`。
    - 戻り値: (tuple): (int スコア, str ステータス説明)。
- **score_calculator.py::calculate_score_change(window_title, config)**:
    - 役割: 設定された正規表現パターンとスコア値のリストに基づき、与えられたウィンドウタイトルがどのパターンにマッチするかを判定し、対応するスコア変化量を決定します。
    - 引数: `window_title` (str), `config` (dict)。
    - 戻り値: (int): スコアの変化量。
- **flow_state_manager.py::update_flow_state(self, current_score_change)**:
    - 役割: 直近のスコア変化量に基づいてユーザーの集中状態（フロー状態）を判断し、ウィンドウの透明度を徐々に変更するかどうかを決定・管理します。
    - 引数: `current_score_change` (int): 直近のスコア増減量。
    - 戻り値: (float): 計算されたウィンドウの現在の透明度（0.0～1.0）。
- **window_behavior.py::manage_always_on_top(self, is_score_decreasing)**:
    - 役割: 設定に基づいてウィンドウを常に最前面に表示するか、またはスコア減少時のみ最前面に表示するかを管理します。
    - 引数: `is_score_decreasing` (bool): スコアが現在減少中であるかどうかのフラグ。
    - 戻り値: なし。
- **window_behavior.py::handle_mouse_proximity(self)**:
    - 役割: マウスカーソルがGUIウィンドウの一定距離内に近づいたときに、ウィンドウを自動的に最背面に移動させ、離れたときに最前面に戻す機能を処理します。
    - 引数: `self`。
    - 戻り値: なし。

## 関数呼び出し階層ツリー
```
main()
├── config.load_app_config()
│   └── config_loader.load_config()
│   └── config_validator.validate_config()
├── gui.GUI(config, score_tracker, flow_state_manager, window_behavior)  (初期化)
│   ├── gui.GUI.update_display()  (定期的に呼び出される)
│   │   ├── window_monitor.get_active_window_title()
│   │   ├── score_tracker.update_score()
│   │   │   └── score_calculator.calculate_score_change()
│   │   ├── score_tracker.get_current_status()
│   │   ├── flow_state_manager.update_flow_state()
│   │   ├── window_behavior.manage_always_on_top()
│   │   └── window_behavior.handle_mouse_proximity()
│   └── gui.GUI.start_update_loop()
├── score_tracker.ScoreTracker(config, score_calculator)  (初期化)
├── flow_state_manager.FlowStateManager(config)  (初期化)
└── window_behavior.WindowBehavior(gui_window, config)  (初期化)

---
Generated at: 2026-02-06 07:08:41 JST
