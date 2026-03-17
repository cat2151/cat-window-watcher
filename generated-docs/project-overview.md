Last updated: 2026-03-18

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、作業内容に基づいてスコアを調整するシンプルなツールです。
- 生産性向上と集中力維持を目的とし、GUIを通じてリアルタイムでスコアを表示します。
- クロスプラットフォームに対応し、正規表現とTOML設定ファイルで柔軟なカスタマイズが可能です。

## 技術スタック
- フロントエンド: Tkinter (Pythonの標準GUIツールキットで、シンプルなユーザーインターフェースを提供します。)
- 音楽・オーディオ: N/A (音楽やオーディオ関連の機能は含まれていません。)
- 開発ツール:
    - Git: ソースコードのバージョン管理に使用されます。
    - pre-commit: コミット前に自動でコードのフォーマットやリンティングを実行し、コード品質を保ちます。
    - Ruff: 高速なPythonリンターおよびフォーマッターとして、コードの品質と一貫性を維持します。
    - unittest: Python標準のテストフレームワークで、主にモジュールの単体テストに使用されます。
    - pytest: 柔軟で拡張可能なPythonテストフレームワークで、効率的なテスト記述と実行をサポートします。
- テスト: unittest, pytest (両フレームワークがPythonコードの単体テストや統合テストに使用され、品質保証に貢献しています。)
- ビルドツール: N/A (Pythonスクリプトとして直接実行されるため、特定のビルドツールは使用されていません。)
- 言語機能:
    - Python 3.12以上: プロジェクトの主要なプログラミング言語です。
    - 正規表現 (reモジュール): ウィンドウタイトルのパターンマッチングに活用されます。
    - TOML: 設定ファイルの記述形式として採用されており、人間が読みやすく、シンプルな構造が特徴です。
- 自動化・CI/CD: pre-commit (コミット前の自動コード品質チェックに利用され、継続的な品質維持に役立ちます。)
- 開発標準:
    - Ruff: コードのフォーマットとリンティングにより、コードスタイルの一貫性を保ち、潜在的な問題を検出します。
    - .editorconfig: 異なるエディタ間でのコーディングスタイル（インデント、改行コードなど）の統一を支援します。

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
  📖 82.md
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
  📄 gui_mock_base.py
  📄 test_config.py
  📄 test_config_flow_mode.py
  📄 test_config_mild_penalty.py
  📄 test_config_self_window_proximity.py
  📄 test_config_transparency.py
  📄 test_config_window_position.py
  📄 test_dummy.py
  📄 test_game_detection.py
  📄 test_gui.py
  📄 test_gui_clipboard.py
  📄 test_gui_flow_mode.py
  📄 test_gui_score_colors.py
  📄 test_gui_score_decreasing.py
  📄 test_gui_status_label.py
  📄 test_gui_transparency.py
  📄 test_score_colors.py
  📄 test_score_tracker.py
  📄 test_score_tracker_flow.py
  📄 test_score_tracker_patterns.py
  📄 test_score_tracker_reset.py
  📄 test_score_tracker_self_window.py
  📄 test_screensaver_detection.py
  📄 test_window_monitor.py
```

## ファイル詳細説明
-   `.editorconfig`: 異なるエディタ間でコードの書式設定（インデント、改行コードなど）を統一するための設定ファイルです。
-   `.gitignore`: Gitのバージョン管理から除外するファイルやディレクトリを指定するファイルです。
-   `.pre-commit-config.yaml`: `pre-commit`フックの設定ファイルで、コミット前に自動的に実行される各種コードチェックツールを定義します。
-   `.vscode/settings.json`: Visual Studio Codeエディタ用のワークスペース設定ファイルです。
-   `LICENSE`: プロジェクトのライセンス情報が記述されています。
-   `README.ja.md`: プロジェクトの日本語版説明書です。概要、機能、使い方などが記載されています。
-   `README.md`: プロジェクトの英語版説明書です。概要、機能、使い方などが記載されています。
-   `_config.yml`: Jekyllなどの静的サイトジェネレーターでドキュメントサイトを構築する際の設定ファイルです。
-   `config.toml.example`: アプリケーション設定ファイル`config.toml`の例で、ウィンドウパターンやスコア設定の参考になります。
-   `docs/`: ドキュメントを格納するディレクトリです。
    -   `game-detection-guide.md`: ゲーム検知に関するガイドラインや情報が記載されたドキュメントです。
-   `examples/`: 様々な設定の例が格納されているディレクトリです。
    -   `README.ja.md`, `README.md`: `examples`ディレクトリの日本語版・英語版説明書です。
    -   `example1_productivity.ja.toml`, `example1_productivity.toml`: 生産性追跡のための設定例（日本語/英語）です。
    -   `example2_study_time.ja.toml`, `example2_study_time.toml`: 勉強時間追跡のための設定例（日本語/英語）です。
    -   `example3_always_on_top.ja.toml`, `example3_always_on_top.toml`: ウィンドウの最前面表示に関する設定例（日本語/英語）です。
-   `generated-docs/`: ドキュメント生成ツールによって生成されたドキュメントが格納される可能性のあるディレクトリです。
-   `issue-notes/`: 開発中の課題や検討事項に関するメモが格納されているディレクトリです。
-   `pytest.ini`: `pytest`テストフレームワークの設定ファイルです。
-   `ruff.toml`: Ruffリンターおよびフォーマッターの設定ファイルです。
-   `src/`: アプリケーションの主要なソースコードが格納されているディレクトリです。
    -   `__init__.py`: Pythonパッケージであることを示すファイルです。
    -   `__main__.py`: モジュールとして実行された際のエントリポイントで、`python -m src`でアプリケーションを起動できます。
    -   `config.py`: アプリケーションのグローバル設定値や設定クラスを定義するモジュールです。
    -   `config_loader.py`: `config.toml`ファイルから設定を読み込むためのロジックを扱うモジュールです。
    -   `config_validator.py`: 読み込まれた設定の妥当性を検証するためのロジックを扱うモジュールです。
    -   `constants.py`: アプリケーション全体で使用される定数を定義するモジュールです。
    -   `flow_state_manager.py`: ユーザーの集中状態（フロー状態）を管理し、それに応じたGUIの振る舞いを制御するモジュールです。
    -   `gui.py`: Tkinterを使用してスコア表示やステータスを表示するグラフィカルユーザーインターフェースを構築するモジュールです。
    -   `main.py`: アプリケーションの主要なエントリポイント。設定の読み込み、GUIの初期化、監視ループの開始などをオーケストレーションします。
    -   `score_calculator.py`: ウィンドウパターンに基づき、具体的なスコアの増減を計算するロジックを提供するモジュールです。
    -   `score_tracker.py`: アクティブなウィンドウタイトルを監視し、設定されたパターンに基づいてスコアを追跡・管理する主要ロジックモジュールです。
    -   `status_formatter.py`: 現在のスコアやアクティブなウィンドウ情報などを、GUIに表示するための形式に整えるモジュールです。
    -   `window_behavior.py`: ウィンドウの挙動（最前面表示、マウス接近時の移動など）を制御するプラットフォーム非依存のロジックを扱うモジュールです。
    -   `window_monitor.py`: アクティブなウィンドウのタイトルをクロスプラットフォームで取得するためのロジックを扱うモジュールです。
-   `tests/`: アプリケーションのテストコードが格納されているディレクトリです。
    -   `gui_mock_base.py`: GUIテスト用のモック基底クラスやヘルパー関数を提供します。
    -   `test_config*.py`: 設定ファイルの読み込み、検証、および各種設定オプション（フローモード、マイルドペナルティ、自己ウィンドウ挙動、透明度、ウィンドウ位置など）に関するテストコードです。
    -   `test_dummy.py`: ダミーのテストファイルです。
    -   `test_game_detection.py`: ゲーム検知機能に関するテストコードです。
    -   `test_gui*.py`: GUIコンポーネントの機能（クリップボード連携、フローモード、スコア表示色、スコア減少時の挙動、ステータスラべル、透明度など）に関するテストコードです。
    -   `test_score_colors.py`: スコア表示色のロジックに関するテストコードです。
    -   `test_score_tracker*.py`: スコア追跡機能の主要ロジック（フロー、パターンマッチング、スコアリセット、自己ウィンドウ挙動など）に関するテストコードです。
    -   `test_screensaver_detection.py`: スクリーンセーバー検知機能に関するテストコードです。
    -   `test_window_monitor.py`: ウィンドウ監視機能に関するテストコードです。

## 関数詳細説明
プロジェクト情報から具体的な関数名とその詳細なシグネチャを直接抽出することはできませんでしたが、各モジュールの役割に基づき、想定される主要な関数の種類と役割について説明します。

-   **`config_loader.py`関連関数**:
    -   `load_config(path: str) -> dict`: 指定されたパスからTOML形式の設定ファイルを読み込み、設定内容を辞書として返します。
-   **`config_validator.py`関連関数**:
    -   `validate_config(config: dict) -> bool`: 読み込まれた設定辞書が、定義されたスキーマやルールに準拠しているか検証し、その結果をブール値で返します。
-   **`window_monitor.py`関連関数**:
    -   `get_active_window_title() -> str`: 現在アクティブなウィンドウのタイトルを文字列で取得します。この関数はLinux, macOS, Windowsの各プラットフォームに対応しています。
    -   `is_screensaver_active() -> bool`: スクリーンセーバーがアクティブな状態であるかを検知し、ブール値でその状態を返します。
-   **`score_tracker.py`関連関数**:
    -   `update_score(window_title: str) -> None`: 現在のウィンドウタイトルに基づいてスコアを計算し、内部のスコア状態を更新します。
    -   `get_current_score() -> int`: 現在の追跡されているスコアの値を整数で返します。
    -   `get_match_description() -> str`: 現在マッチしているウィンドウパターンの説明文を文字列で返します。
    -   `reset_score() -> None`: 現在のスコアを0にリセットします。
-   **`score_calculator.py`関連関数**:
    -   `calculate_score_change(window_title: str, config: dict) -> int`: 指定されたウィンドウタイトルとアプリケーション設定に基づいて、スコアの増減値を計算し、整数で返します。
-   **`flow_state_manager.py`関連関数**:
    -   `update_flow_state(score_change: int) -> None`: スコアの変化量に基づいて、ユーザーの集中状態（フロー状態）を更新します。
    -   `is_in_flow_mode() -> bool`: 現在フローモードであるかをブール値で返します。
    -   `get_current_transparency() -> float`: 現在のフロー状態や設定に応じたウィンドウの透明度（0.0〜1.0）を返します。
-   **`status_formatter.py`関連関数**:
    -   `format_status(score: int, description: str, score_change: int) -> str`: 現在のスコア、アクティビティの説明、スコアの変化量を元に、GUIに表示するための整形されたステータス文字列を生成します。
-   **`window_behavior.py`関連関数**:
    -   `set_always_on_top(window_id: int, always_on_top: bool) -> None`: 指定されたウィンドウIDのウィンドウを常に最前面に表示するかどうかを設定します。
    -   `check_mouse_proximity(window_id: int, distance: int) -> bool`: マウスカーソルが指定されたウィンドウに一定の距離（`distance`）以内に近づいているかをチェックし、ブール値で返します。
    -   `set_window_transparency(window_id: int, alpha: float) -> None`: 指定されたウィンドウIDのウィンドウの透明度を設定します（`alpha`は0.0〜1.0の範囲）。
-   **`gui.py`関連関数**:
    -   `__init__(master)`: GUIアプリケーションのメインウィンドウと、スコアやステータスを表示するための各種ウィジェットを初期化します。
    -   `update_gui() -> None`: 定期的に呼ばれ、現在のスコアやアクティビティの説明に基づいてGUI表示を更新します。
    -   `start_gui_loop() -> None`: Tkinterのイベントループを開始し、GUIを表示・操作可能にします。
-   **`main.py`関連関数**:
    -   `main() -> None`: アプリケーションの主要なエントリポイント関数です。設定の読み込み、GUIの初期化、ウィンドウ監視ループの開始といった、アプリケーション全体のオーケストレーションを行います。

## 関数呼び出し階層ツリー
```
プロジェクト情報からは、関数間の具体的な呼び出し階層を分析できませんでした。

---
Generated at: 2026-03-18 07:12:12 JST
