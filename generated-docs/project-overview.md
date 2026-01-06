Last updated: 2026-01-07

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、あなたの作業内容に基づいてスコアを調整する、シンプルでスタンドアロンなツールです。
- 「猫」があなたの作業状況を監視しているというコンセプトで、生産的な活動でスコアが上がり、非生産的な活動でスコアが下がります。
- カスタマイズ可能な正規表現ベースのウィンドウマッチング、tkinterによるGUI表示、クロスプラットフォーム対応が特徴です。

## 技術スタック
- フロントエンド: **tkinter**: Python標準のGUIライブラリで、シンプルでクリーンなユーザーインターフェースを提供します。
- 音楽・オーディオ: 該当する技術は使用されていません。
- 開発ツール: **Python**: アプリケーションの主要なプログラミング言語。**git**: バージョン管理システム。**ruff**: Pythonコードのフォーマットとリンティング（コード品質検査）に使用。**pre-commit**: コミット前にコード品質チェックを自動実行するためのツール。
- テスト: **unittest**: Python標準のテストフレームワークで、各モモジュールの機能が期待通りに動作するかを検証します。
- ビルドツール: 該当するビルドツールは使用されていません。本プロジェクトはPythonスクリプトとして直接実行されます。
- 言語機能: **正規表現 (regex)**: ウィンドウタイトルをパターンマッチングするために使用。**TOML**: 設定ファイル（`config.toml`）の記述形式として使用され、人間が読み書きしやすい構造を提供します。
- 自動化・CI/CD: **pre-commit**: コミット前の自動化されたコード品質チェックにより、開発標準の維持を支援します。
- 開発標準: **ruff**: コードスタイルと品質を統一し、レビューとメンテナンスを容易にします。**.editorconfig**: 複数のエディタ間でコーディングスタイルを統一するための設定ファイルです。

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
- **`.editorconfig`**: 複数の開発者が異なるエディタを使用しても、インデントスタイルや文字コードなどのコーディングスタイルを統一するための設定ファイルです。
- **`.gitignore`**: Gitがバージョン管理の対象から外すファイルやディレクトリ（例: 自動生成ファイル、一時ファイル）を指定します。
- **`.pre-commit-config.yaml`**: Gitのコミット前に自動的に実行されるフック（例: コードフォーマットやリンティング）の設定を定義し、コード品質の維持を助けます。
- **`.vscode/settings.json`**: Visual Studio Codeエディタにおける、このプロジェクト固有の設定を格納します。
- **`LICENSE`**: プロジェクトの利用条件や配布に関するライセンス情報が記載されています。
- **`README.ja.md`**: プロジェクトの目的、機能、インストール方法、使い方などが日本語で記述された主要な説明書です。
- **`README.md`**: プロジェクトの目的、機能、インストール方法、使い方などが英語で記述された主要な説明書です。
- **`_config.yml`**: GitHub Pagesなどの静的サイトジェネレータ（例: Jekyll）で使用される設定ファイルです。
- **`config.toml.example`**: `config.toml`を作成する際のテンプレートとなる設定ファイルで、ウィンドウパターンやスコア設定の記述例が含まれています。
- **`examples/example.txt`**: プロジェクトの特定の機能やユースケースを示すための追加のサンプルファイルが含まれるディレクトリです。
- **`generated-docs/`**: 自動生成されたドキュメントやレポートを格納するためのディレクトリです。
- **`issue-notes/`**: 開発中に発生した個別の課題（Issue）に関するメモや詳細情報をまとめたファイル群です（開発者向け情報）。
- **`pytest.ini`**: Pythonのテストフレームワークであるpytestの設定ファイルです。
- **`ruff.toml`**: Pythonの高速なリンターおよびフォーマッターであるRuffの設定ファイルで、コードスタイルと品質のルールを定義します。
- **`src/`**: アプリケーションの主要なソースコードが配置されているディレクトリです。
    - **`src/__init__.py`**: `src`ディレクトリがPythonパッケージであることを示すファイルです。
    - **`src/__main__.py`**: `python -m src`のようにモジュールとして実行された際のエントリポイントとなります。
    - **`src/config.py`**: `config.toml`ファイルからアプリケーションの設定を読み込み、管理する役割を担います。
    - **`src/constants.py`**: アプリケーション全体で共通して使用される定数（例:マジックナンバー、パスなど）を定義します。
    - **`src/gui.py`**: `tkinter`ライブラリを使用して、スコア表示やステータス表示を行うグラフィカルユーザーインターフェース（GUI）を構築します。
    - **`src/main.py`**: アプリケーションのメインのエントリポイントです。設定の読み込み、GUIの初期化、ウィンドウ監視ループの開始と調整を行います。
    - **`src/score_tracker.py`**: アクティブなウィンドウタイトルを正規表現パターンに照合し、それに基づいてスコアを計算・追跡するロジックを管理します。
    - **`src/window_monitor.py`**: 現在アクティブなウィンドウのタイトルを、オペレーティングシステム（Linux, macOS, Windows）に依存しない方法で取得する機能を提供します。
- **`tests/`**: アプリケーションの各モジュールに対する単体テストコードが配置されているディレクトリです。
    - **`tests/test_config.py`**: `src/config.py`モジュールの機能（設定ファイルの読み込みなど）をテストします。
    - **`tests/test_dummy.py`**: 初期開発段階や特定の目的で作成されたダミーのテストファイルです。
    - **`tests/test_gui.py`**: `src/gui.py`モジュールのGUI表示やインタラクションに関する機能をテストします。
    - **`tests/test_score_colors.py`**: スコアの増減に応じた色の表示ロジックをテストします。
    - **`tests/test_score_tracker.py`**: `src/score_tracker.py`モジュールのスコア計算および追跡ロジックをテストします。
    - **`tests/test_window_monitor.py`**: `src/window_monitor.py`モジュールのウィンドウタイトル取得機能が正しく動作するかをテストします。

## 関数詳細説明
※プロジェクト情報から具体的な関数名は提供されていないため、主要なモジュールの役割に基づいた代表的な関数とその説明を記述します。

- **`main.py`**
    - `main()`: アプリケーション全体の実行フローを制御するメイン関数です。設定の読み込み、GUIの初期化、定期的なウィンドウ監視とスコア更新のループを開始します。
- **`config.py`**
    - `load_config(path: str) -> dict`: 指定されたパスのTOML設定ファイルを読み込み、その内容を辞書形式で返します。
    - `get_setting(key: str, default_value: Any) -> Any`: 設定データから指定されたキーの値を取得します。キーが存在しない場合は、提供されたデフォルト値を返します。
- **`window_monitor.py`**
    - `get_active_window_title() -> str`: 現在システム上でアクティブになっているウィンドウのタイトルを取得して文字列として返します。これはOS間で異なるAPIを使用して実現されます。
- **`score_tracker.py`**
    - `ScoreTracker(config: dict)`: スコアを追跡するクラスのコンストラクタです。初期スコアや設定情報を基に、スコア計算のためのパターンを準備します。
    - `update_score(window_title: str) -> Tuple[int, str]`: 与えられたウィンドウタイトルと設定されたパターンを照合し、スコアを更新します。更新後のスコアと、マッチしたパターンの説明（もしあれば）を返します。
    - `get_current_score() -> int`: 現在のスコアの値を返します。
    - `reset_score()`: 現在のスコアをゼロ（または設定された初期値）にリセットします。
- **`gui.py`**
    - `CatWindowWatcherGUI(root: tk.Tk, initial_score: int, config: dict)`: `tkinter`ウィンドウを初期化し、スコアやステータスを表示するためのGUI要素（ラベル、フレームなど）を設定します。
    - `update_display(score: int, description: str, score_change: int)`: GUI上のスコア表示、アクティビティの説明、スコアの変化に応じた色などをリアルタイムで更新します。
    - `run()`: `tkinter`イベントループを開始し、GUIアプリケーションを動作させます。
    - `apply_always_on_top(enabled: bool)`: ウィンドウを他のウィンドウの上に常に表示するかどうかを切り替えます。
    - `fade_window(transparency: float)`: ウィンドウの透明度を設定し、徐々に透明にしたり不透明にしたりする効果を適用します。

## 関数呼び出し階層ツリー
※詳細な関数呼び出し階層は提供されていないため、主要モジュール間の高レベルな連携を示します。
```
main.py (アプリケーションのエントリポイント)
├── config.py::load_config (設定ファイルの読み込み)
├── gui.py::CatWindowWatcherGUI (GUIの初期化)
│   └── gui.py::update_display (GUI表示の更新)
├── score_tracker.py::ScoreTracker (スコア追跡ロジックの初期化)
│   └── score_tracker.py::update_score (ウィンドウタイトルに基づくスコア更新)
└── (メインループ内で定期的に呼び出し)
    ├── window_monitor.py::get_active_window_title (アクティブウィンドウタイトルの取得)
    ├── score_tracker.py::update_score (取得したタイトルでスコア更新)
    └── gui.py::update_display (更新されたスコアをGUIに反映)

---
Generated at: 2026-01-07 07:06:13 JST
