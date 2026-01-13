Last updated: 2026-01-14

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、あなたの作業内容に基づいてスコアを調整するシンプルなスタンドアロンツールです。
- GitHubでの作業でスコアが上昇し、SNS閲覧でスコアが減少するなど、生産性を楽しく可視化します。
- Tkinter製のクリーンなGUI、正規表現ベースの設定、クロスプラットフォーム対応が特徴の軽量アプリケーションです。

## 技術スタック
- フロントエンド: `tkinter` (Python標準のGUIライブラリで、シンプルでクリーンなユーザーインターフェースを提供します。)
- 音楽・オーディオ: (このプロジェクトでは音楽・オーディオ関連技術は使用されていません。)
- 開発ツール: `Git` (バージョン管理システム), `VS Code` (設定ファイルが提供されており、開発環境の統一を支援します), `Pre-commit` (コミット前のフックを設定し、コード品質を自動でチェックします)。
- テスト: `unittest` (Python標準の単体テストフレームワーク), `pytest` (より高度なテスト機能とシンプルな記述を提供するPythonのテストフレームワーク)。
- ビルドツール: (このプロジェクトではPythonスクリプトを直接実行するため、特定のビルドツールは使用していません。)
- 言語機能: `Python 3.12+` (プロジェクトの主要な開発言語および実行環境), `正規表現` (ウィンドウタイトルとのマッチングに利用されます), `TOML` (設定ファイルの記述形式として使用されます)。
- 自動化・CI/CD: `Pre-commit` (コミットフックにより、コードフォーマットやリンティングの自動化を実現します)。
- 開発標準: `ruff` (高速なPythonリンターおよびフォーマッターで、コード品質と一貫性を保ちます), `.editorconfig` (異なるIDEやエディタ間でのコーディングスタイルの一貫性を維持します)。
- プラットフォーム固有ライブラリ: `xdotool` / `xprop` (Linuxでのウィンドウタイトル取得に必要), `AppleScript` (macOSでのウィンドウタイトル取得に利用される内蔵機能), `pywin32` (Windowsでのウィンドウタイトル取得を強化するオプションライブラリ)。

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
- **`.editorconfig`**: 異なるエディタやIDE間で一貫したコーディングスタイルを維持するための設定ファイルです。
- **`.gitignore`**: Gitがバージョン管理の対象外とするファイルやディレクトリを指定します。
- **`.pre-commit-config.yaml`**: Gitコミット前に自動でコードの整形や品質チェックを行うためのPre-commitフックの設定ファイルです。
- **`.vscode/settings.json`**: Visual Studio Codeエディタにおける、このプロジェクト固有の設定を定義します。
- **`LICENSE`**: このソフトウェアの利用条件を定めるライセンス情報が記述されています。
- **`README.ja.md`**: プロジェクトの日本語版説明書です。
- **`README.md`**: プロジェクトの英語版説明書です。
- **`_config.yml`**: Jekyllなどの静的サイトジェネレーターで利用される設定ファイルですが、このプロジェクトでは直接の用途は示されていません。
- **`config.toml.example`**: ユーザーがアプリケーションの設定をカスタマイズするための、TOML形式の設定例ファイルです。
- **`examples/`**: 様々な使用シナリオに対応する設定例が格納されているディレクトリです。
    - **`examples/README.ja.md`**: `examples`ディレクトリの日本語版説明書です。
    - **`examples/README.md`**: `examples`ディレクトリの英語版説明書です。
    - **`examples/example*.toml`**: 生産性の追跡、勉強時間、特定のGUI挙動などの設定例ファイル群です。
- **`generated-docs/`**: 自動生成されたドキュメントが格納される可能性のあるディレクトリです。
- **`pytest.ini`**: Pythonのテストフレームワーク`pytest`の設定ファイルです。
- **`ruff.toml`**: Pythonのリンターおよびフォーマッターである`ruff`の設定ファイルです。
- **`src/`**: アプリケーションの主要なソースコードが格納されているディレクトリです。
    - **`src/__init__.py`**: `src`ディレクトリをPythonパッケージとして認識させるためのファイルです。
    - **`src/__main__.py`**: `python -m src`のようにモジュールとして実行された際のエントリポイントです。
    - **`src/config.py`**: アプリケーション全体で使用される設定値を構造化して管理するモジュールです。
    - **`src/config_loader.py`**: `config.toml`ファイルから設定を読み込み、Pythonオブジェクトに変換する役割を担います。
    - **`src/config_validator.py`**: 読み込まれた設定値が正しい形式や範囲内であるかを検証するモジュールです。
    - **`src/constants.py`**: アプリケーション全体で共有される不変の定数を定義します。
    - **`src/flow_state_manager.py`**: ユーザーの集中状態（フロー状態）を管理し、それに応じてGUIの透明度などを調整するモジュールです。
    - **`src/gui.py`**: `tkinter`ライブラリを使用して、スコアやステータスを表示するユーザーインターフェースを構築・管理するモジュールです。
    - **`src/main.py`**: アプリケーションの起動スクリプトであり、各モジュールを統合して全体の処理フローを制御します。
    - **`src/score_calculator.py`**: アクティブなウィンドウタイトルと設定されたパターンに基づいて、スコアの増減量を計算するロジックを提供します。
    - **`src/score_tracker.py`**: 現在のスコアを保持し、時間経過やアクティビティに基づいてスコアを更新・管理するモジュールです。
    - **`src/status_formatter.py`**: GUIに表示される現在の活動やスコア変化に関するテキストを整形するユーティリティです。
    - **`src/window_behavior.py`**: GUIウィンドウの「常に最前面表示」や、マウス接近時の自動的な最背面移動といった特殊な挙動を制御するモジュールです。
    - **`src/window_monitor.py`**: OSの機能（xdotool, AppleScript, WinAPIなど）を利用して、現在アクティブなウィンドウのタイトルを取得するクロスプラットフォーム対応モジュールです。
- **`tests/`**: アプリケーションの各コンポーネントの機能が正しく動作するかを検証するためのテストコードが格納されているディレクトリです。
    - **`tests/test_config.py`**: 設定の読み込みと検証機能に関するテストです。
    - **`tests/test_dummy.py`**: 開発初期の簡単なテストやテンプレートとして利用されるテストファイルです。
    - **`tests/test_gui.py`**: GUIの表示やインタラクションに関するテストです。
    - **`tests/test_score_colors.py`**: スコアの変化に応じたGUI表示色の変更ロジックに関するテストです。
    - **`tests/test_score_tracker.py`**: スコア追跡と更新のロジックに関するテストです。
    - **`tests/test_screensaver_detection.py`**: スクリーンセーバーがアクティブな状態を検出する機能に関するテストです。
    - **`tests/test_window_monitor.py`**: ウィンドウタイトル取得機能のテストです。

## 関数詳細説明
プロジェクト情報から具体的な関数情報を検出できませんでしたが、主要なモジュールから推測される代表的な関数をリストアップします。

- **`main.py`**
    - `main()`:
        - **役割**: アプリケーションのエントリポイント。設定の読み込み、GUIの初期化、監視ループの開始、各種モジュールの連携をオーケストレーションします。
        - **引数**: なし（コマンドライン引数を受け取る可能性があります）。
        - **戻り値**: なし。

- **`src/config_loader.py`**
    - `load_config(config_path)`:
        - **役割**: 指定されたパスのTOML設定ファイルを読み込み、設定オブジェクトとして返します。
        - **引数**: `config_path` (str): 設定ファイルのパス。
        - **戻り値**: 設定オブジェクト (dict-like object)。

- **`src/gui.py`**
    - `CatWindowWatcherGUI.__init__(self, master, config, update_callback)`:
        - **役割**: GUIウィンドウを初期化し、スコア表示、ステータス表示などのウィジェットを配置します。タイマーベースのGUI更新ループを設定します。
        - **引数**: `master` (tk.Tk): Tkinterのルートウィンドウ。`config` (object): 設定オブジェクト。`update_callback` (callable): 定期的に呼び出される更新処理のコールバック関数。
        - **戻り値**: なし。
    - `CatWindowWatcherGUI.update_display(self, score, status_text, score_change_direction)`:
        - **役割**: GUI上のスコア表示とステータス表示を最新の情報に更新します。スコアの変化方向に応じて色を調整します。
        - **引数**: `score` (int): 現在のスコア。`status_text` (str): 現在の活動を示すテキスト。`score_change_direction` (str): スコアが上昇('up')、下降('down')、変化なし('none')を示す文字列。
        - **戻り値**: なし。

- **`src/window_monitor.py`**
    - `get_active_window_title()`:
        - **役割**: 現在OS上でアクティブになっているウィンドウのタイトルを取得します。OSごとに内部実装が異なります。
        - **引数**: なし。
        - **戻り値**: アクティブなウィンドウのタイトル (str)。タイトルが取得できない場合は空文字列。

- **`src/score_tracker.py`**
    - `ScoreTracker.__init__(self, config)`:
        - **役割**: スコアトラッカーのインスタンスを初期化します。設定オブジェクトを内部に保持します。
        - **引数**: `config` (object): 設定オブジェクト。
        - **戻り値**: なし。
    - `ScoreTracker.process_window_title(self, window_title)`:
        - **役割**: 与えられたウィンドウタイトルに基づいてスコアを更新し、その変化量と方向を返します。
        - **引数**: `window_title` (str): 現在アクティブなウィンドウのタイトル。
        - **戻り値**: `(score_change, description, score_change_direction)` (tuple): スコアの変化量、マッチしたパターンの説明、スコアの変化方向。
    - `ScoreTracker.get_current_score(self)`:
        - **役割**: 現在の累積スコアを取得します。
        - **引数**: なし。
        - **戻り値**: 現在のスコア (int)。

- **`src/score_calculator.py`**
    - `calculate_score_change(active_window_title, config)`:
        - **役割**: アクティブなウィンドウタイトルが設定されたどのパターンにマッチするかを評価し、対応するスコアの変化量と説明を計算します。
        - **引数**: `active_window_title` (str): 現在アクティブなウィンドウのタイトル。`config` (object): 設定オブジェクト。
        - **戻り値**: `(score_value, description)` (tuple): 計算されたスコア値と、それに紐づく説明。

- **`src/flow_state_manager.py`**
    - `FlowStateManager.__init__(self, config, gui)`:
        - **役割**: フロー状態マネージャーを初期化します。GUIオブジェクトと設定を保持します。
        - **引数**: `config` (object): 設定オブジェクト。`gui` (CatWindowWatcherGUI): GUIインスタンス。
        - **戻り値**: なし。
    - `FlowStateManager.update_flow_state(self, score_change_direction)`:
        - **役割**: スコアの変化方向に基づいてフロー状態を更新し、設定に応じてウィンドウの透明度を調整します。
        - **引数**: `score_change_direction` (str): スコアの変化方向 ('up', 'down', 'none')。
        - **戻り値**: なし。

- **`src/window_behavior.py`**
    - `apply_window_behavior(gui_root, window_title_to_copy, current_score_change_direction, config)`:
        - **役割**: 設定に基づいて、ウィンドウの「常に最前面表示」や、マウス接近時の挙動、スコア減少時の特別な表示、クリップボードへのコピーなど、GUIウィンドウの様々な動作を適用します。
        - **引数**: `gui_root` (tk.Tk): GUIのルートウィンドウ。`window_title_to_copy` (str): クリップボードにコピーされるべきウィンドウタイトル。`current_score_change_direction` (str): 現在のスコアの変化方向。`config` (object): 設定オブジェクト。
        - **戻り値**: なし。

## 関数呼び出し階層ツリー
プロジェクト情報から具体的な関数呼び出し階層を検出できませんでした。ここでは、主要なモジュールと関数間の一般的な連携フローを推測して表現します。

```
main.py
└── main()
    ├── config_loader.load_config()
    ├── gui.CatWindowWatcherGUI.__init__()
    │   └── gui.CatWindowWatcherGUI.start_update_loop() (内部で_update_app_stateを呼び出し)
    ├── score_tracker.ScoreTracker.__init__()
    ├── flow_state_manager.FlowStateManager.__init__()
    └── _update_app_state() (GUIループから定期的に呼び出される内部処理)
        ├── window_monitor.get_active_window_title()
        ├── score_tracker.process_window_title()
        │   └── score_calculator.calculate_score_change()
        ├── flow_state_manager.update_flow_state()
        ├── window_behavior.apply_window_behavior()
        └── gui.CatWindowWatcherGUI.update_display()

---
Generated at: 2026-01-14 07:06:26 JST
