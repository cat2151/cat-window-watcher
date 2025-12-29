Last updated: 2025-12-30

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、作業内容に応じてスコアをリアルタイムに表示するツールです。
- 定義したルールに基づいて生産性や集中度をスコア化し、自己管理をサポートします。
- シンプルなGUIとクロスプラットフォーム対応で、猫があなたを見守るコンセプトで動機付けを促します。

## 技術スタック
- フロントエンド: **tkinter**: Python標準のGUIライブラリで、シンプルかつ軽量なユーザーインターフェースを提供します。
- 音楽・オーディオ: (該当する技術はありません)
- 開発ツール:
    - **Git**: ソースコードのバージョン管理システムとして利用されています。
    - **ruff**: Pythonコードのフォーマットとリンティングを高速に行い、コード品質を保ちます。
    - **pre-commit**: コミット前に自動的にコードの品質チェック（フォーマット、リンティングなど）を実行するフックを設定します。
    - **VS Code**: `.vscode/settings.json`により、Visual Studio Codeでの開発環境設定が管理されています。
    - **EditorConfig**: 複数のエディタやIDE間でコーディングスタイルの一貫性を保つための設定ファイルです。
- テスト:
    - **unittest**: Python標準のテストフレームワークで、モジュールや関数の単体テストに使用されます。
    - **pytest**: 高機能で拡張性の高いテストフレームワークで、柔軟なテスト記述と実行を可能にします。
- ビルドツール: (Pythonスクリプトのため、専用のビルドツールは使用していません)
- 言語機能:
    - **Python**: プロジェクトの主要なプログラミング言語です。
    - **正規表現**: ウィンドウタイトルのパターンマッチングに利用され、柔軟なルール設定を可能にします。
- 自動化・CI/CD:
    - **pre-commit**: ローカルでのコミット前フックによるコード品質の自動チェックが導入されています。
- 開発標準:
    - **ruff**: コードのフォーマットとリンティングにより、一貫したコーディングスタイルと品質を維持します。
    - **EditorConfig**: 複数環境でのコーディングスタイル統一に貢献します。

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
  📖 4.md
  📖 6.md
  📖 8.md
  📖 9.md
📄 pytest.ini
📄 ruff.toml
📁 src/
  📄 __init__.py
  📄 __main__.py
  📄 config.py
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
- **`.editorconfig`**: 異なるエディタやIDE間で一貫したコーディングスタイル（インデント、改行コードなど）を定義するための設定ファイルです。
- **`.gitignore`**: Gitのバージョン管理から除外するファイルやディレクトリを指定します（例: 一時ファイル、ビルド成果物）。
- **`.pre-commit-config.yaml`**: Gitコミット前に自動でコード整形やリンティングなどのチェックを実行するための設定ファイルです。
- **`.vscode/settings.json`**: Visual Studio Codeエディタにおけるこのプロジェクト固有の設定（ワークスペース設定）を定義します。
- **`LICENSE`**: このプロジェクトのソフトウェアライセンス（利用条件）が記載されています。
- **`README.ja.md`**: プロジェクトの概要、機能、インストール方法、設定、使い方、開発方法などが日本語でまとめられたドキュメントです。
- **`README.md`**: プロジェクトの概要、機能、インストール方法、設定、使い方、開発方法などが英語でまとめられたドキュメントです。
- **`_config.yml`**: 一般的にはGitHub Pagesなどの静的サイトジェネレーターで利用される設定ファイルですが、このプロジェクトでの具体的な用途は明示されていません。
- **`config.toml.example`**: アプリケーションの設定ファイル（`config.toml`）のサンプルです。ユーザーはこのファイルをコピーして独自の設定を作成します。
- **`examples/example.txt`**: 使用例やサンプルデータなどを格納するディレクトリ内のファイルです。
- **`generated-docs/`**: 自動生成されたドキュメント（APIドキュメントなど）が格納されることを想定したディレクトリです。
- **`issue-notes/`**: 開発中の課題や検討事項に関するメモがIssue番号ごとに格納されています（開発者向け情報）。
- **`pytest.ini`**: Pythonのテストフレームワークである`pytest`の設定ファイルです。
- **`ruff.toml`**: 高速リンター/フォーマッタである`ruff`の設定ファイルです。
- **`src/__init__.py`**: `src`ディレクトリがPythonパッケージであることを示します。
- **`src/__main__.py`**: `python -m src`のようにモジュールとして実行された際のエントリポイントです。
- **`src/config.py`**: アプリケーションの設定ファイル（`config.toml`）の読み込みと管理を担うモジュールです。
- **`src/gui.py`**: `tkinter`を使用して、スコア表示や現在のアクティビティなどのグラフィカルユーザーインターフェースを構築・管理するモジュールです。
- **`src/main.py`**: アプリケーションの主要なエントリポイントであり、各モジュールの調整（オーケストレーション）とメインループの管理を行います。
- **`src/score_tracker.py`**: アクティブなウィンドウタイトルを定義されたパターンと照合し、スコアの計算と追跡を行うロジックを実装したモジュールです。
- **`src/window_monitor.py`**: Windows、macOS、Linuxといった異なるOS上で、現在アクティブなウィンドウのタイトルを取得するクロスプラットフォームな機能を提供するモジュールです。
- **`tests/`**: アプリケーションの各モジュールに対する単体テストや統合テストのコードを格納するディレクトリです。

## 関数詳細説明
- **`main.py` の `run_app()`**:
    - **役割**: アプリケーション全体の起動とメインループの管理を担います。設定の読み込み、GUIの初期化、ウィンドウ監視とスコア更新の定期的な実行を調整します。
    - **機能**: アプリケーションのコアロジックを統合し、ユーザーインターフェースを介して結果を表示します。
- **`config.py` の `load_config(path)`**:
    - **役割**: 指定されたパスからTOML形式の設定ファイルを読み込み、アプリケーションが使用する設定データを提供します。
    - **機能**: ウィンドウパターン、スコアの増減値、UIの挙動に関する設定などをパースして利用可能にします。
- **`window_monitor.py` の `get_active_window_title()`**:
    - **役割**: 現在アクティブになっている（ユーザーが操作している）ウィンドウのタイトルを取得します。
    - **機能**: OS固有のAPI（Linuxではxdotool/xprop、macOSではAppleScript、Windowsでは内蔵API）を利用して、クロスプラットフォームで動作します。
- **`score_tracker.py` の `ScoreTracker` クラス**:
    - **役割**: 定義された正規表現パターンとアクティブなウィンドウタイトルを照合し、それに基づいてスコアを計算・更新・追跡します。
    - **機能**: スコアの増減、デフォルトスコアの適用、スコアのリセットなど、スコア管理に関するすべてのロジックをカプセル化します。
- **`gui.py` の `CatWindowWatcherGUI` クラス**:
    - **役割**: `tkinter`ライブラリを用いて、アプリケーションのグラフィカルユーザーインターフェースを構築し、スコアや現在の活動状況を表示します。
    - **機能**: スコアのリアルタイム更新、アクティブなパターンの表示、ウィンドウの最前面表示やマウス接近時の挙動といったUI設定を管理します。

## 関数呼び出し階層ツリー
```
run_app() (src/main.py)
├── config.load_config() (src/config.py)
├── CatWindowWatcherGUI.start_gui() (src/gui.py)
│   └── CatWindowWatcherGUI.update_loop() (定期的なGUI更新とロジック実行)
│       ├── window_monitor.get_active_window_title() (src/window_monitor.py)
│       ├── ScoreTracker.update_score() (src/score_tracker.py)
│       └── CatWindowWatcherGUI.update_display() (src/gui.py)
└── ScoreTracker.__init__() (src/score_tracker.py)

---
Generated at: 2025-12-30 07:06:07 JST
