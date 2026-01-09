Last updated: 2026-01-10

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、ユーザーの生産性に基づいてスコアを調整するツールです。
- ウィンドウタイトルにマッチするパターンを設定し、生産的な活動でスコアを増加、集中を阻害する活動で減少させます。
- シンプルなTkinter GUI、クロスプラットフォーム対応、軽量な設計で、ユーザーの集中をサポートします。

## 技術スタック
- フロントエンド: **tkinter** (Python標準のGUIライブラリで、シンプルかつクリーンなユーザーインターフェースを提供します。)
- 音楽・オーディオ: (特になし)
- 開発ツール: **Git** (バージョン管理システム), **unittest**, **pytest** (Pythonの単体テストフレームワーク), **ruff** (Pythonコードの高速なリンター兼フォーマッター), **pre-commit** (Gitコミット前に指定されたフックを自動実行し、コード品質を維持します。)
- テスト: **unittest** (Pythonの標準テストフレームワーク), **pytest** (テストの実行と管理をより効率的に行うためのフレームワークです。)
- ビルドツール: 本プロジェクトはPythonスクリプトを直接実行するため、特定のビルドツールは使用していません。Python 3.12以上の環境で動作します。
- 言語機能: **Python 3.12以上** (主要な開発言語および実行環境), **正規表現** (ウィンドウタイトルのパターンマッチングに活用されます。)
- 自動化・CI/CD: **pre-commit** (コードのフォーマットやリンティングをコミット時に自動化し、品質の維持に貢献します。)
- 開発標準: **ruff** (コードスタイルの一貫性と品質を強制するためのルールセットを提供します), **.editorconfig** (異なるエディタやIDE間で一貫したコーディングスタイルを定義します。)
- プラットフォーム固有API: Linux (`xdotool`, `xprop`), macOS (`AppleScript`), Windows (`pywin32`または内蔵API) を使用してアクティブなウィンドウタイトルを取得します。

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
-   `.editorconfig`: 異なる開発環境（エディタやIDE）間でインデントスタイルや文字コードなど、基本的なコーディングスタイルの一貫性を保つための設定ファイルです。
-   `.gitignore`: Gitのバージョン管理システムが無視すべきファイルやディレクトリ（例: ログファイル、ビルド成果物、一時ファイルなど）を指定します。
-   `.pre-commit-config.yaml`: `pre-commit`フレームワークの設定ファイル。コミット前に`ruff format`や`ruff check`などの自動チェックを実行し、コード品質を確保します。
-   `.vscode/settings.json`: Visual Studio Codeエディタのワークスペース固有の設定を定義し、プロジェクトチーム内での開発環境の一貫性を高めます。
-   `LICENSE`: 本プロジェクトのソフトウェアライセンス（利用条件、著作権など）が記載されています。
-   `README.ja.md`: プロジェクトの目的、機能、インストール方法、設定例、使用方法などを日本語で詳細に説明するメインドキュメントです。
-   `README.md`: プロジェクトの目的、機能、インストール方法、設定例、使用方法などを英語で詳細に説明するメインドキュメントです。
-   `_config.yml`: Jekyllなどの静的サイトジェネレータで使用される設定ファイルで、サイトのビルドに関するメタデータやオプションを定義します。
-   `config.toml.example`: `config.toml`ファイルを作成する際のテンプレートとして提供される設定ファイルです。ウィンドウパターンやスコア設定の例が含まれています。
-   `pytest.ini`: `pytest`テストフレームワークの動作をカスタマイズするための設定ファイルです。
-   `ruff.toml`: `ruff`リンター/フォーマッターの詳細な設定を定義するファイルで、Pythonコードのスタイルと品質に関するルールを管理します。
-   `src/__init__.py`: `src`ディレクトリをPythonパッケージとして認識させるための空ファイルです。
-   `src/__main__.py`: `python -m src`のようにモジュールとして実行された際のエントリポイントです。通常は`main.py`の`run_app`関数を呼び出します。
-   `src/config.py`: アプリケーションのランタイム設定を保持するデータ構造や、その設定へのアクセスを提供するモジュールです。
-   `src/config_loader.py`: `config.toml`ファイルから設定を読み込み、Pythonオブジェクトとして解析する機能を提供します。
-   `src/config_validator.py`: 読み込まれた設定値がアプリケーションの要件（型、範囲など）に合致しているかを検証するロジックを実装します。
-   `src/constants.py`: アプリケーション全体で使用される固定値、例えばUIのカラーコード、デフォルトのスコア値などを一元的に管理します。
-   `src/flow_state_manager.py`: ユーザーが集中状態（「フロー状態」）にあるかどうかを判定し、それに基づいてGUIの透過度を調整するなどのロジックを管理します。
-   `src/gui.py`: PythonのTkinterライブラリを使用して、スコアと現在のアクティビティを表示するグラフィカルユーザーインターフェースを構築します。
-   `src/main.py`: アプリケーションのメインエントリポイントであり、各モジュールを初期化し、ウィンドウ監視ループを調整して、アプリケーション全体の動作をオーケストレーションします。
-   `src/score_calculator.py`: 現在のアクティブウィンドウタイトルとユーザー定義のパターンに基づいて、スコアの増減量を計算するコアロジックを実装します。
-   `src/score_tracker.py`: ユーザーの現在のスコアを保持し、`score_calculator`からの結果を受け取ってスコアを更新・管理する役割を担います。
-   `src/status_formatter.py`: GUIに表示されるスコアやステータス（例: "GitHub (+10)"）のテキストを、見やすく整形する機能を提供します。
-   `src/window_behavior.py`: アプリケーションウィンドウの特定の挙動（例: 常に最前面表示、マウスが近づいた際の自動非表示、スコア減少時の強調表示など）を管理します。
-   `src/window_monitor.py`: OS固有のAPIを利用して、現在フォーカスされているウィンドウのタイトルを取得するクロスプラットフォームな機能を提供します。
-   `tests/test_config.py`: 設定ファイルの読み込み、パース、検証に関する単体テストを記述します。
-   `tests/test_dummy.py`: 開発初期段階などで使用される可能性のある、シンプルなテストのプレースホルダーです。
-   `tests/test_gui.py`: TkinterベースのGUIコンポーネントが正しく動作し、適切に表示されるかを検証するテストです。
-   `tests/test_score_colors.py`: スコアの増減に応じたGUIの色変更ロジックに関するテストです。
-   `tests/test_score_tracker.py`: スコアの計算、更新、リセットなど、スコア追跡機能の正確性を検証するテストです。
-   `tests/test_screensaver_detection.py`: スクリーンセーバーがアクティブな状態を検出する機能（もしあれば）のテストです。
-   `tests/test_window_monitor.py`: アクティブウィンドウタイトルの取得機能が、異なるOSやシナリオで正しく動作するかを検証するテストです。

## 関数詳細説明
-   **`main.py` 内の主要な関数**:
    -   `run_app(config_path)`: アプリケーションのメインエントリポイントとして機能します。設定を読み込み、GUIを初期化し、定期的なウィンドウ監視とスコア更新タスクを開始します。
        -   引数: `config_path` (str) - 設定ファイルのパス。
        -   戻り値: なし。
-   **`config_loader.py` 内の主要な関数**:
    -   `load_config(config_path)`: 指定されたパスにあるTOML形式の設定ファイルを読み込み、それをPythonの辞書またはオブジェクト形式で返します。
        -   引数: `config_path` (str) - 読み込む設定ファイルのパス。
        -   戻り値: `config_data` (dict/object) - 読み込まれた設定データ。
-   **`config_validator.py` 内の主要な関数**:
    -   `validate_config(config)`: 読み込まれた設定データが、アプリケーションの動作に必要なすべてのキーを含み、値の型や範囲が適切であるかを検証します。無効な場合はエラーを発生させるか、デフォルト値を適用します。
        -   引数: `config` (dict/object) - 検証する設定データ。
        -   戻り値: (bool) - 設定が有効であれば`True`、そうでなければ`False`。
-   **`window_monitor.py` 内の主要な関数**:
    -   `get_active_window_title()`: 現在フォーカスされている最前面のウィンドウのタイトルを取得します。内部でOS固有のAPI呼び出しを抽象化しています。
        -   引数: なし。
        -   戻り値: `title` (str) - アクティブなウィンドウのタイトル。取得できない場合は空文字列。
-   **`score_tracker.py` 内の主要な関数**:
    -   `update_score(window_title)`: 与えられたウィンドウタイトルを基に、設定されたパターンと照合し、現在のスコアを計算・更新します。スコアの増減量も返します。
        -   引数: `window_title` (str) - 現在アクティブなウィンドウのタイトル。
        -   戻り値: `score_change` (int) - 今回の更新でスコアが変化した量。
    -   `get_current_score()`: 現在追跡されているスコアの合計値を取得します。
        -   引数: なし。
        -   戻り値: `current_score` (int) - 現在のスコアの合計値。
-   **`score_calculator.py` 内の主要な関数**:
    -   `calculate_score_change(window_title, patterns, default_score, self_window_score, ...)`: ウィンドウタイトルと設定されたパターンリストを比較し、そのマッチ結果に基づいてスコアの増減値を決定します。デフォルトスコアや自身のウィンドウに対するスコアも考慮します。
        -   引数: `window_title` (str), `patterns` (list), `default_score` (int) など。
        -   戻り値: `calculated_score_delta` (int) - 計算されたスコアの変化量。
-   **`gui.py` 内の主要な関数**:
    -   `init_gui(root, config)`: Tkinterのルートウィンドウとアプリケーション設定を受け取り、スコア表示、ステータス表示などのGUI要素を構築し初期化します。
        -   引数: `root` (tkinter.Tk) - Tkinterのルートウィンドウ, `config` (object) - アプリケーション設定。
        -   戻り値: GUIの表示を更新するためのインターフェースオブジェクト。
    -   `update_display(score, status_text, score_color, current_transparency)`: GUI上のスコア、ステータス、色、透明度をリアルタイムで更新し、ユーザーに表示します。
        -   引数: `score` (int), `status_text` (str), `score_color` (str), `current_transparency` (float)。
        -   戻り値: なし。
-   **`window_behavior.py` 内の主要な関数**:
    -   `apply_window_settings(root, config_manager, gui_manager)`: `always_on_top`や`hide_on_mouse_proximity`などの設定に基づいて、GUIウィンドウの表示挙動（最前面表示、マウス接近時の移動など）を設定し、動的に制御します。
        -   引数: `root` (tkinter.Tk), `config_manager` (object), `gui_manager` (object)。
        -   戻り値: なし。
-   **`flow_state_manager.py` 内の主要な関数**:
    -   `update_flow_state(score_change)`: スコアの変化（特にスコア上昇）を監視し、ユーザーが一定時間「フロー状態」にあるかを判定します。フロー状態が継続している場合、ウィンドウの透過度調整をトリガーします。
        -   引数: `score_change` (int) - 前回の更新でのスコア変化量。
        -   戻り値: (bool) - 現在フロー状態が有効であれば`True`。

## 関数呼び出し階層ツリー
```
main.py (アプリケーションのエントリポイントと主制御ループ)
├── run_app()
    ├── config_loader.load_config()                 (設定ファイルの読み込み)
    ├── config_validator.validate_config()          (読み込んだ設定の検証)
    ├── gui.init_gui()                              (GUIの初期化と構築)
    ├── window_behavior.apply_window_settings()     (ウィンドウ挙動の設定)
    ├── <定期的に実行されるタスク (例: update_task)>
    │   ├── window_monitor.get_active_window_title() (アクティブウィンドウタイトルの取得)
    │   ├── score_tracker.update_score()             (スコアの更新)
    │   │   └── score_calculator.calculate_score_change() (スコア変化量の計算)
    │   ├── flow_state_manager.update_flow_state()   (フロー状態の更新と管理)
    │   ├── score_tracker.get_current_score()        (現在のスコアの取得)
    │   ├── status_formatter.format_status()         (ステータス表示テキストの整形)
    │   └── gui.update_display()                     (GUIの表示更新)
    └── tkinter.mainloop()                          (GUIイベントループの開始)

---
Generated at: 2026-01-10 07:06:36 JST
