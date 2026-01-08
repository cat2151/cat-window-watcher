Last updated: 2026-01-09

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、あなたの作業内容に基づいて生産性スコアをリアルタイムで表示します。
- GitHubでの作業はスコアが上がり、SNS閲覧は下がるなど、カスタマイズ可能なパターンで評価します。
- シンプルなGUIとクロスプラットフォーム対応により、自己管理を支援する軽量なツールです。

## 技術スタック
- フロントエンド: **tkinter** (Python標準のGUIライブラリ。シンプルで直感的なスコア表示インターフェースに使用されています。)
- 音楽・オーディオ: (該当なし)
- 開発ツール: **Git** (ソースコードのバージョン管理に使用されます。)、 **pre-commit** (コミット前のコード品質チェックを自動化します。)、 **ruff** (Pythonの高速なリンター兼フォーマッターで、コード品質とスタイルを維持します。)、 **xdotool** / **xprop** (Linuxシステムでアクティブなウィンドウのタイトルを取得するために使用されます。)、 **AppleScript** (macOSシステムでウィンドウタイトルを取得するために使用される組み込みスクリプトです。)、 **pywin32** (Windowsシステムでより良い互換性のためにオプションで使用されるWindows API連携ライブラリです。)
- テスト: **unittest** (Python標準のテストフレームワークで、各モジュールの機能が正しく動作することを確認するために使用されます。)
- ビルドツール: (このプロジェクトはPythonスクリプトとして直接実行されるため、特定のビルドツールは使用されていません。)
- 言語機能: **Python 3.12+** (プロジェクトの主要な開発言語であり、実行環境として推奨されています。)、 **正規表現 (Regex)** (ウィンドウタイトルをパターンマッチングしてスコアを決定するために使用されます。)、 **TOML** (設定ファイルを記述するためのシンプルで人間が読めるファイル形式です。)
- 自動化・CI/CD: **pre-commit** (コミット前に自動でコードフォーマットやリンティングを行い、継続的な品質維持を支援します。)
- 開発標準: **.editorconfig** (異なるエディタ間でのコードスタイルの一貫性を保証します。)、 **ruff** (コードのスタイルと品質に関するルールを適用し、統一された開発標準を維持します。)

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
- **.editorconfig**: 異なる開発環境間でのコードスタイル（インデント、改行など）の統一を定義するファイルです。
- **.gitignore**: Gitがバージョン管理の対象としないファイルやディレクトリを指定するファイルです。
- **.pre-commit-config.yaml**: Gitコミット前に自動実行されるフック（linting, formattingなど）を設定するファイルです。
- **.vscode/settings.json**: Visual Studio Codeエディタにおけるこのプロジェクト固有の設定を定義します。
- **LICENSE**: 本プロジェクトの利用条件とライセンス情報を記載しています。
- **README.ja.md**: プロジェクトの目的、機能、使用方法などを日本語で説明するドキュメントです。
- **README.md**: プロジェクトの目的、機能、使用方法などを英語で説明する主要ドキュメントです。
- **_config.yml**: GitHub Pagesなどで使用される設定ファイルで、サイトの構成を定義します。
- **config.toml.example**: ユーザーがコピーしてカスタマイズできる、設定ファイルの例です。
- **examples/example.txt**: プロジェクトの機能やデータ形式を示すための例示ファイルです。
- **generated-docs/**: 自動生成されたドキュメントやレポートが格納される可能性のあるディレクトリです。
- **issue-notes/**: 開発過程で発生した課題や検討事項に関するノートが格納されているディレクトリです。
- **pytest.ini**: Pythonのテストフレームワークpytestの設定ファイルですが、本プロジェクトのテスト実行には主に`unittest`が使用されています。
- **ruff.toml**: Pythonの高速リンター/フォーマッターである`ruff`の設定ファイルで、コード品質ルールを定義します。
- **src/__init__.py**: `src`ディレクトリがPythonパッケージであることを示すファイルです。
- **src/__main__.py**: `python -m src`のようにモジュールとして実行された際のエントリポイントとなるファイルです。
- **src/config.py**: アプリケーションの実行時設定を管理し、他のモジュールが設定値にアクセスするためのインターフェースを提供します。
- **src/config_loader.py**: TOML形式の設定ファイルを読み込み、アプリケーションが利用できる形式に変換する機能を提供します。
- **src/config_validator.py**: 読み込まれた設定値が正しい形式であり、有効な範囲内にあるかを検証するロジックを含みます。
- **src/constants.py**: アプリケーション全体で共通して使用される定数（例えば、ウィンドウタイトルなど）を定義します。
- **src/flow_state_manager.py**: スコアの上昇・下降トレンドを検知し、「フロー状態」に応じてウィンドウの透明度や挙動を管理します。
- **src/gui.py**: PythonのTkinterライブラリを使用して、スコアや現在のアクティビティを表示するグラフィカルユーザーインターフェースを構築します。
- **src/main.py**: アプリケーションの主要なエントリポイントです。設定の読み込み、GUIの初期化、ウィンドウ監視ループの開始と調整を行います。
- **src/score_calculator.py**: アクティブなウィンドウタイトルと定義されたパターンに基づいて、スコアの増減量を計算するロジックを提供します。
- **src/score_tracker.py**: 現在の生産性スコアを保持し、時間経過や`score_calculator`からの入力に基づいてスコアを更新・管理します。
- **src/status_formatter.py**: 現在のマッチパターンやウィンドウタイトルを、GUIに表示しやすい形式に整形する役割を担います。
- **src/window_behavior.py**: ウィンドウの「常に最前面表示」や「マウス接近時の非表示」といった、GUIウィンドウの特殊な挙動を制御するロジックを実装します。
- **src/window_monitor.py**: OS（Linux, macOS, Windows）ごとのAPIやツールを利用して、現在アクティブなウィンドウのタイトルを取得する機能を提供します。
- **tests/test_config.py**: 設定ファイルの読み込みや検証ロジックが正しく機能するかを検証するテストです。
- **tests/test_dummy.py**: 初期開発段階やテンプレートとして用意されたダミーのテストファイルです。
- **tests/test_gui.py**: GUIの表示更新やユーザーインタラクションに関連する機能が正しく動作するかを検証するテストです。
- **tests/test_score_colors.py**: スコアの変化に応じてGUIの色が変わるロジックを検証するテストです。
- **tests/test_score_tracker.py**: スコアの計算、更新、リセットなど、スコア追跡のコアロジックを検証するテストです。
- **tests/test_screensaver_detection.py**: スクリーンセーバーがアクティブな状態を検出する機能（もしあれば）を検証するテストです。
- **tests/test_window_monitor.py**: 異なるOS環境下でウィンドウタイトルを正確に取得できるかを検証するテストです。

## 関数詳細説明
主要モジュールの主要関数について概説します。具体的な引数、戻り値、実装詳細はソースコードをご参照ください。

- **`main.py`**
    - `main()`: アプリケーションのメインエントリポイント。設定のロード、GUIの初期化と開始、定期的なウィンドウ監視とスコア更新のループをオーケストレートします。
- **`config_loader.py`**
    - `load_config(config_path)`: 指定されたパスからTOML形式の設定ファイルを読み込み、アプリケーションで使用できる設定オブジェクトを生成します。
- **`window_monitor.py`**
    - `get_active_window_title()`: 現在アクティブなウィンドウのタイトルを、実行環境のOSに応じた方法で取得し、文字列として返します。
- **`score_calculator.py`**
    - `calculate_score_change(active_window_title, config_patterns)`: アクティブなウィンドウタイトルと設定ファイルで定義されたパターンを比較し、適用されるスコアの変化量（増減値）を計算して返します。
- **`score_tracker.py`**
    - `update_score(score_change)`: 計算されたスコアの変化量に基づいて、現在のスコアを更新します。
    - `get_current_score()`: 現在のスコアの値を返します。
    - `reset_score_if_needed(current_time)`: 設定されたリセット間隔（例: 30分ごと）に基づいて、スコアを0にリセットする必要があるかを判断し、実行します。
- **`gui.py`**
    - `update_gui(score, status_text, score_color)`: GUI上のスコア表示とステータステキストを更新し、スコアの増減に応じて表示色を調整します。
    - `start_gui(update_callback)`: Tkinter GUIアプリケーションのメインループを開始し、定期的な更新処理のためのコールバック関数を設定します。
- **`flow_state_manager.py`**
    - `update_flow_state(current_score_change)`: 最新のスコア変化に基づいてフロー状態（集中状態）を更新し、ウィンドウの透明度や表示挙動に影響を与える場合があります。
- **`window_behavior.py`**
    - `apply_window_behavior(root_window, config)`: 設定に基づいて、ウィンドウを常に最前面に表示したり、マウスが近づいたときに一時的に最背面に移動させたりするなどの特殊な挙動を適用します。

## 関数呼び出し階層ツリー
```
main.py (main関数)
├── config_loader.py (load_config)
├── gui.py (start_gui)
│   └── gui.py (update_gui) - ※ mainループから定期的に呼び出される
├── (メインループ内で定期的に実行)
│   ├── window_monitor.py (get_active_window_title)
│   ├── score_calculator.py (calculate_score_change)
│   ├── score_tracker.py (update_score)
│   │   └── score_tracker.py (reset_score_if_needed)
│   ├── status_formatter.py (format_status_text)
│   ├── flow_state_manager.py (update_flow_state)
│   └── window_behavior.py (apply_window_behavior または関連関数)
└── (GUIイベントハンドラやタイマースレッドから)
    └── window_behavior.py (例えば、マウス移動イベントでウィンドウ位置や状態を調整する関数)
```
このツリーは、主要なモジュールと関数間の呼び出し関係を簡略化して示しています。`main.py`の`main`関数がアプリケーションの起点となり、設定の読み込み、GUIの起動、そしてメインループ内での定期的な処理（ウィンドウ監視、スコア計算・更新、GUI更新、特殊なウィンドウ挙動の適用など）を調整します。GUIの更新はメインループから、またはGUIイベントループ内でトリガーされます。

---
Generated at: 2026-01-09 07:06:23 JST
