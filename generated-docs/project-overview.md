Last updated: 2025-12-29

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、作業内容に基づいて生産性スコアを調整するシンプルなツールです。
- ウィンドウタイトルに合わせた正規表現ベースのマッチングとスコア設定が可能で、クロスプラットフォームで動作します。
- 「猫があなたを見ている」というコンセプトのもと、軽量で分かりやすいGUIで作業状況を可視化します。

## 技術スタック
- フロントエンド: **tkinter**: Python標準のGUIツールキットで、軽量かつシンプルなユーザーインターフェースを提供します。
- 音楽・オーディオ: 該当なし
- 開発ツール:
    - **Git**: ソースコードのバージョン管理システム。
    - **GitHub**: Gitリポジトリのホスティングサービスおよび共同開発プラットフォーム。
    - **.editorconfig**: 異なるエディタやIDE間で一貫したコーディングスタイルを維持するための設定ファイル。
    - **VS Code (settings.json)**: Visual Studio Codeエディタのワークスペース固有の設定ファイル。
- テスト:
    - **unittest**: Python標準の単体テストフレームワーク。
    - **pytest**: Python用の人気のあるテストフレームワークで、unittestよりも簡潔なテスト記述が可能です。
- ビルドツール: 該当なし (Pythonスクリプトとして直接実行されるため、専用のビルドツールは使用していません)
- 言語機能:
    - **Python 3.12+**: プロジェクトの主要開発言語。高い可読性と豊富なライブラリが特徴です。
    - **正規表現 (reモジュール)**: ウィンドウタイトルのパターンマッチングに利用されます。
    - **TOML**: 設定ファイル (`config.toml`) のフォーマットとして使用され、人間が読み書きしやすいシンプルな構造を提供します。
    - **プラットフォーム固有API連携**:
        - Linux: `xdotool` または `xprop` コマンドを通じてウィンドウ情報を取得します。
        - macOS: 内蔵のAppleScriptを通じてウィンドウ情報を取得します。
        - Windows: 内蔵のWindows API、またはオプションで`pywin32`ライブラリを通じてウィンドウ情報を取得します。
- 自動化・CI/CD:
    - **pre-commit**: コミット前にコードのフォーマットチェックやリンティングを自動実行するためのフレームワーク。
- 開発標準:
    - **ruff**: Pythonの高速リンターおよびフォーマッターで、コード品質の維持と統一されたコーディングスタイルを強制します。
    - **.editorconfig**: コードスタイルの統一。
    - **ruff.toml**: `ruff`の設定ファイル。

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
  4.md
  6.md
  8.md
  9.md
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
  test_gui.py
  test_score_tracker.py
  test_window_monitor.py
```

## ファイル詳細説明
- **`.editorconfig`**: さまざまなエディタやIDEで、インデントスタイルや文字コードなどの基本的なコーディング規約を統一するための設定ファイルです。
- **`.gitignore`**: Gitがバージョン管理の対象としないファイルやディレクトリのパターンを定義します。ビルド生成物や一時ファイルなどが含まれます。
- **`.pre-commit-config.yaml`**: Gitコミット前に自動で実行されるフック（処理）を設定します。コードのフォーマットチェックやリンティングなどに使われます。
- **`.vscode/settings.json`**: Visual Studio Codeエディタのワークスペース（このプロジェクト）固有の設定を定義します。
- **`LICENSE`**: プロジェクトの利用条件を定めるライセンス情報が記述されています。
- **`README.ja.md` / `README.md`**: プロジェクトの概要、機能、インストール方法、使用方法、設定、開発ガイドなど、ユーザーや開発者向けの基本的な情報が記述されたドキュメントです（日本語版と英語版）。
- **`_config.yml`**: GitHub Pagesなどの設定に用いられることが多いファイルです。
- **`config.toml.example`**: ユーザーがコピーしてカスタマイズするための設定ファイル`config.toml`のサンプルです。ウィンドウパターンやスコア、UIの動作設定などが含まれます。
- **`examples/`**: プロジェクトに関連する使用例や参考となるファイルが格納されるディレクトリです。
- **`generated-docs/`**: 自動生成されたドキュメントやレポートなどを格納するためのディレクトリです。
- **`issue-notes/`**: 開発中の課題や特定の機能に関するメモ、検討事項などが記録されたファイルが格納されているディレクトリです。
- **`pytest.ini`**: `pytest`テストフレームワークの設定ファイルです。テストの発見方法やオプションなどを定義します。
- **`ruff.toml`**: Pythonのリンター・フォーマッターである`ruff`の設定ファイルです。コードスタイルのルールやチェック項目を定義します。
- **`src/__init__.py`**: Pythonのパッケージであることを示すファイルです。通常は空か、パッケージレベルの初期化コードを含みます。
- **`src/__main__.py`**: `python -m src`のようにモジュールとして実行された際のエントリーポイントとなるファイルです。通常、`main.py`の処理を呼び出します。
- **`src/config.py`**: TOML形式の設定ファイル (`config.toml`) を読み込み、アプリケーション全体で利用可能な形で管理するロジックを提供します。
- **`src/gui.py`**: tkinterを使用して、スコア表示や現在のアクティビティを表示するグラフィカルユーザーインターフェース (GUI) を構築し、管理します。
- **`src/main.py`**: アプリケーションの主要なエントリーポイントです。設定のロード、GUIの初期化、ウィンドウ監視ループの開始と停止など、全体のオーケストレーションを担います。
- **`src/score_tracker.py`**: アクティブなウィンドウタイトルを正規表現パターンと照合し、設定されたルールに基づいてスコアを増減させ、その履歴と現在の状態を追跡します。
- **`src/window_monitor.py`**: 現在アクティブなウィンドウのタイトルを、OS（Linux, macOS, Windows）に応じた方法で取得するためのクロスプラットフォームなロジックを提供します。
- **`tests/`**: プロジェクトの各モジュールのテストコードを格納するディレクトリです。
    - **`tests/test_config.py`**: `src/config.py`モジュールの機能に関するテストを行います。
    - **`tests/test_dummy.py`**: テストのプレースホルダー、または簡単なテストケースを保持するファイルです。
    - **`tests/test_gui.py`**: `src/gui.py`モジュールのGUIコンポーネントに関するテストを行います。
    - **`tests/test_score_tracker.py`**: `src/score_tracker.py`モジュールのスコア計算および追跡ロジックに関するテストを行います。
    - **`tests/test_window_monitor.py`**: `src/window_monitor.py`モジュールのウィンドウタイトル取得機能に関するテストを行います。

## 関数詳細説明
このプロジェクトは、複数のモジュールに機能を分割しており、それぞれのモジュールが以下の主要な役割を果たす関数群を持っています。

-   **`main.py` の主要関数**:
    -   `main()`: プログラムの起動時に呼び出されるメイン関数。アプリケーション全体の設定を初期化し、GUIと監視ロジックを連携させてアプリケーションの実行を管理します。
    -   `run_app(config_path)`: コマンドライン引数で指定された設定ファイルパスに基づき、アプリケーションの実行フローを管理する関数。

-   **`config.py` の主要関数**:
    -   `load_config(file_path)`: 指定されたTOML形式のファイルパスから設定データを読み込み、アプリケーションで利用しやすいオブジェクト形式で返します。
    -   `get_default_config()`: 設定ファイルが存在しない場合や、一部の設定が不足している場合に、アプリケーションのデフォルト設定値を生成して提供します。

-   **`window_monitor.py` の主要関数**:
    -   `get_active_window_title()`: 現在アクティブな（最前面に表示されている）ウィンドウのタイトルバーテキストを取得します。この関数は内部でOSごとの実装（Linux, macOS, Windows）を呼び分けます。
    -   `_get_title_linux()`: Linux環境で`xdotool`や`xprop`コマンドを利用してウィンドウタイトルを取得する内部ヘルパー関数。
    -   `_get_title_macos()`: macOS環境でAppleScriptを利用してウィンドウタイトルを取得する内部ヘルパー関数。
    -   `_get_title_windows()`: Windows環境でWindows API（オプションで`pywin32`）を利用してウィンドウタイトルを取得する内部ヘルパー関数。

-   **`score_tracker.py` の主要クラスとメソッド**:
    -   `ScoreTracker(config)`: スコア追跡のロジックをカプセル化するクラスのコンストラクタ。設定情報に基づいて、ウィンドウパターンとそれに対応するスコア変化量を初期化します。
    -   `update_score(window_title)`: 与えられたウィンドウタイトルを正規表現パターンと照合し、マッチしたパターンに基づいて現在のスコアを更新します。
    -   `get_current_score()`: 現在の累積スコアの値を返します。
    -   `get_current_description()`: 現在マッチしているウィンドウパターンに対応する説明文字列を返します。

-   **`gui.py` の主要クラスとメソッド**:
    -   `CatWindowWatcherGUI(root, score_tracker, config)`: tkinterのルートウィンドウ（`root`）、`ScoreTracker`インスタンス、および設定情報を受け取り、GUIの全ての要素を初期化し表示するクラスのコンストラクタ。
    -   `update_display()`: GUI上のスコア表示と現在のアクティビティ説明を定期的に更新し、最新の状態を反映させます。
    -   `_setup_ui()`: ウィンドウタイトル、スコア表示ラベル、ステータス表示ラベルなど、GUIのレイアウトと各ウィジェット（部品）を設定する内部ヘルパー関数。
    -   `_start_update_loop()`: GUIの表示を一定間隔（例: 1秒ごと）で自動更新するためのタイマーループを開始します。
    -   `_check_mouse_proximity()`: マウスカーソルがGUIウィンドウに近づいた際に、ウィンドウの表示順序（最前面・最背面）を自動で切り替える機能のロジックを実装した内部関数。
    -   `_toggle_always_on_top(is_top)`: ウィンドウが常に他のウィンドウの上に表示されるかどうかを切り替える関数です。

## 関数呼び出し階層ツリー
```
main.py (アプリケーションのエントリポイント)
├── run_app()
│   ├── config.py (設定の読み込み)
│   │   └── load_config(file_path)
│   ├── score_tracker.py (スコア追跡ロジックの初期化)
│   │   └── ScoreTracker(config)
│   └── gui.py (GUIの初期化と表示)
│       └── CatWindowWatcherGUI(root, score_tracker, config)
│           ├── _setup_ui()
│           └── _start_update_loop() (定期的なGUI更新ループ)
│               ├── score_tracker.py (スコアの取得・更新)
│               │   ├── update_score(window_title)
│               │   │   └── window_monitor.py (ウィンドウタイトルの取得)
│               │   │       └── get_active_window_title()
│               │   │           ├── _get_title_linux()
│               │   │           ├── _get_title_macos()
│               │   │           └── _get_title_windows()
│               │   ├── get_current_score()
│               │   └── get_current_description()
│               ├── update_display() (GUI表示の更新)
│               └── _check_mouse_proximity() (マウス接近チェック)

---
Generated at: 2025-12-29 07:05:57 JST
