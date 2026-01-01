Last updated: 2026-01-02

# Project Overview

## プロジェクト概要
- アクティブなウィンドウを監視し、生産性向上と集中力維持を支援するスタンドアロンのツールです。
- ウィンドウタイトルに基づきスコアをリアルタイムで調整し、GitHub作業でスコアアップ、SNS閲覧でスコアダウンといったルールを設定できます。
- シンプルなGUIで現在のスコアと活動を表示し、クロスプラットフォームで軽量に動作するよう設計されています。

## 技術スタック
- フロントエンド: **Tkinter**: Python標準のGUIライブラリで、シンプルかつ軽量なユーザーインターフェースを構築するために使用されています。
- 音楽・オーディオ: (該当する技術はありません)
- 開発ツール:
    - **Git**: 分散型バージョン管理システム。ソースコードの変更履歴を管理し、共同開発を支援します。
    - **.editorconfig**: 異なるエディタやIDEを使用する開発者間で、インデントスタイルや文字コードなどのコーディングスタイルを統一するための設定ファイルです。
    - **.pre-commit**: Gitコミット前に指定されたスクリプト（LinterやFormatterなど）を自動実行し、コード品質を保つためのフレームワークです。
    - **VS Code 設定**: Visual Studio Codeエディタのワークスペース固有の設定ファイル（`.vscode/settings.json`）で、開発環境を最適化します。
    - **ruff**: Python用の非常に高速なLinterおよびFormatterです。コードの構文チェック、スタイルガイドの強制、自動フォーマットを行います。
    - **pytest.ini**: Pythonのテストフレームワークであるpytestの設定ファイルです。テストの発見方法や実行オプションなどを定義します。
- テスト:
    - **unittest**: Python標準ライブラリに含まれる単体テストフレームワーク。各コンポーネントの機能が正しく動作するかを検証します。
    - **pytest**: Pythonコミュニティで広く使われている、機能豊富で拡張性の高いテストフレームワークです。
- ビルドツール: (該当するビルドツールはありません。本プロジェクトはPythonスクリプトとして直接実行されます。)
- 言語機能: **Python 3.12以上**: アプリケーションの中核をなすプログラミング言語です。最新の言語機能と性能を活用しています。
- 自動化・CI/CD: **pre-commit**: コミット前にコード品質チェックやフォーマットを自動実行するフック管理ツールです。
- 開発標準: **ruff**: 統一されたコードスタイルと品質を強制するために使用されます。
- OS連携:
    - **xdotool / xprop**: Linux環境で現在アクティブなウィンドウのタイトルを取得するために使用されるコマンドラインツールです。
    - **AppleScript**: macOS環境でウィンドウ情報を取得するために使用される組み込みのスクリプト言語サポートです。
    - **pywin32**: Windows環境でWindows APIを通じてウィンドウ情報を取得するためにオプションで使用されるPythonライブラリです。

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
- **.editorconfig**: 異なる開発環境でコードスタイル（インデント、文字コードなど）を統一するための設定ファイルです。
- **.gitignore**: Gitがバージョン管理の対象としないファイルやディレクトリを指定するファイルです。
- **.pre-commit-config.yaml**: Gitコミット時に自動実行されるフック（LinterやFormatterなど）の設定を定義するファイルです。
- **.vscode/settings.json**: Visual Studio Codeエディタのワークスペース固有の設定ファイルで、開発環境の挙動をカスタマイズします。
- **LICENSE**: 本プロジェクトのソフトウェアライセンス情報（例: MITライセンス）が記述されたファイルです。
- **README.ja.md**: プロジェクトの日本語版説明書です。機能、インストール方法、設定、使用法などが記載されています。
- **README.md**: プロジェクトの英語版説明書です。日本語版と同様の内容が英語で記述されています。
- **_config.yml**: GitHub Pagesなどの静的サイトジェネレーターで利用される可能性のある設定ファイルです。
- **config.toml.example**: アプリケーション設定ファイル `config.toml` のテンプレートです。ユーザーがこれをコピーしてカスタマイズするための参考として提供されます。
- **examples/example.txt**: プロジェクトの使用例やサンプルデータなどを格納するディレクトリです。
- **generated-docs/**: 自動生成されたドキュメントや資料を格納するためのディレクトリです。
- **pytest.ini**: Pythonのテストフレームワーク `pytest` の設定ファイルです。テスト実行時のオプションなどを指定します。
- **ruff.toml**: PythonのLinterおよびFormatterである `ruff` の設定ファイルです。コードスタイルや静的解析のルールを定義します。
- **src/__init__.py**: `src` ディレクトリがPythonパッケージであることを示すファイルです。
- **src/__main__.py**: `python -m src` のようにモジュールとして実行された際のエントリポイントで、通常は `main.py` を呼び出します。
- **src/config.py**: TOML形式の設定ファイルを読み込み、アプリケーション全体で利用可能な設定オブジェクトを提供するモジュールです。
- **src/constants.py**: アプリケーション内で使用される共通の定数やマジックナンバーなどを定義するモジュールです。
- **src/gui.py**: `tkinter` を使用して、現在のスコアやアクティビティを表示するグラフィカルユーザーインターフェース（GUI）を構築・管理するモジュールです。
- **src/main.py**: アプリケーションのメインエントリポイントです。各モジュールをオーケストレーションし、ウィンドウ監視ループとGUIの更新を制御します。
- **src/score_tracker.py**: アクティブなウィンドウタイトルを定義済みパターンとマッチさせ、それに基づいてスコアを計算・更新するロジックを管理するモジュールです。
- **src/window_monitor.py**: OS固有のAPI（Linux: `xdotool`/`xprop`、macOS: `AppleScript`、Windows: `pywin32`または内蔵API）を使用して、現在アクティブなウィンドウのタイトルを取得するモジュールです。
- **tests/test_config.py**: `src/config.py` モジュールの設定読み込み機能に関する単体テストを記述したファイルです。
- **tests/test_dummy.py**: テストスイートが適切に機能するか確認するためのダミーのテストファイルです。
- **tests/test_gui.py**: `src/gui.py` モジュールのGUI表示や更新機能に関する単体テストを記述したファイルです。
- **tests/test_score_colors.py**: スコア表示の色分け機能に関する単体テストを記述したファイルです。
- **tests/test_score_tracker.py**: `src/score_tracker.py` モジュールのスコア計算ロジックに関する単体テストを記述したファイルです。
- **tests/test_window_monitor.py**: `src/window_monitor.py` モジュールのウィンドウタイトル取得機能に関する単体テストを記述したファイルです。

## 関数詳細説明
- **config.py**:
    - `load_config(config_path: str = "config.toml") -> dict`:
        - **役割**: 指定されたパスからTOML形式の設定ファイルを読み込みます。
        - **引数**: `config_path` (str, オプション): 設定ファイルのパス。デフォルトは"config.toml"。
        - **戻り値**: 辞書形式で読み込んだ設定データ。
        - **機能**: 設定ファイルが存在しない場合や一部の設定が欠けている場合は、適切なデフォルト値を適用し、アプリケーションが安定して動作するようにします。
- **window_monitor.py**:
    - `get_active_window_title() -> str`:
        - **役割**: 現在アクティブな（フォーカスされている）ウィンドウのタイトルを取得します。
        - **引数**: なし。
        - **戻り値**: アクティブなウィンドウのタイトル文字列。取得に失敗した場合は空文字列を返す可能性があります。
        - **機能**: OSの機能（Linuxの`xdotool`、macOSのAppleScript、Windows APIなど）を抽象化し、クロスプラットフォームで動作するように実装されています。
- **score_tracker.py**:
    - `ScoreTracker` クラス: アプリケーションのスコア管理とロジックをカプセル化します。
        - `__init__(config: dict)`:
            - **役割**: `ScoreTracker` のインスタンスを初期化します。
            - **引数**: `config` (dict): アプリケーション全体の設定情報。
            - **機能**: 設定情報に基づいて、スコアの初期値、ウィンドウパターン、ペナルティモードなどの動作パラメータを設定します。
        - `update_score(window_title: str) -> tuple[int, str]`:
            - **役割**: 提供されたウィンドウタイトルに基づいてスコアを更新します。
            - **引数**: `window_title` (str): 現在アクティブなウィンドウのタイトル。
            - **戻り値**: 更新後の現在のスコア (int) と、マッチしたパターンの説明文字列 (str) のタプル。
            - **機能**: ウィンドウタイトルを正規表現パターンと比較し、マッチしたパターンに応じたスコアの増減を適用します。また、リセットやペナルティモードなどの設定も考慮します。
        - `reset_score()`:
            - **役割**: 現在のスコアを0にリセットします。
            - **引数**: なし。
            - **戻り値**: なし。
            - **機能**: 主に定期的なスコアリセット機能（例: 30分ごと）によって呼び出され、新しい集中期間を開始します。
        - `get_current_score() -> int`:
            - **役割**: 現在のスコアを取得します。
            - **引数**: なし。
            - **戻り値**: 現在のスコアの整数値。
            - **機能**: GUI表示など、現在のスコアを参照する際に利用されます。
        - `is_score_decreasing() -> bool`:
            - **役割**: スコアが現在減少傾向にあるかどうかを判定します。
            - **引数**: なし。
            - **戻り値**: スコアが減少中であれば `True`、そうでなければ `False`。
            - **機能**: ウィンドウの常に最前面表示（`always_on_top_while_score_decreasing`）などの挙動を制御するために使用されます。
        - `is_flow_mode_active() -> bool`:
            - **役割**: フローモードが現在アクティブであるかどうかを判定します。
            - **引数**: なし。
            - **戻り値**: フローモードが有効であれば `True`、そうでなければ `False`。
            - **機能**: スコアが上昇し続け、集中状態にあると判断された場合にウィンドウの透明度を調整するなどの視覚効果を制御します。
        - `get_fade_opacity() -> float`:
            - **役割**: フローモード時にウィンドウに適用する透明度（不透明度）を計算します。
            - **引数**: なし。
            - **戻り値**: 0.0 (完全に透明) から 1.0 (完全に不透明) の間の浮動小数点数。
            - **機能**: フローモードの遅延やフェード速度設定に基づいて、ウィンドウの透明度を徐々に変化させます。
- **gui.py**:
    - `CatWindowWatcherGUI` クラス: TkinterベースのGUIを構築・管理します。
        - `__init__(master, config: dict, score_tracker)`:
            - **役割**: GUIウィンドウとそのコンポーネントを初期化します。
            - **引数**: `master` (tk.Tk): Tkinterのルートウィンドウ。`config` (dict): アプリケーション設定。`score_tracker` (ScoreTracker): スコア管理インスタンス。
            - **機能**: Tkinterのラベル、フレームなどを配置し、初期スコアとメッセージを表示します。ウィンドウの最前面表示やマウス接近時の挙動も設定します。
        - `update_display(score: int, activity_description: str, is_score_decreasing: bool)`:
            - **役割**: GUI上のスコア表示とアクティビティ説明を更新します。
            - **引数**: `score` (int): 現在のスコア。`activity_description` (str): 現在の活動説明。`is_score_decreasing` (bool): スコアが減少中か。
            - **機能**: スコアの数値と説明テキストを更新し、スコアの増減に応じて表示色を変更したり、フローモードに応じてウィンドウの透明度を調整したりします。
        - `start_periodic_update(interval_ms: int, callback)`:
            - **役割**: 指定された間隔で特定のコールバック関数を繰り返し実行するタイマーを開始します。
            - **引数**: `interval_ms` (int): 更新間隔（ミリ秒）。`callback` (callable): 繰り返し実行する関数。
            - **機能**: アプリケーションのメインループ内で、定期的にウィンドウ監視とGUI更新の処理をトリガーします。
        - `hide_window()`:
            - **役割**: GUIウィンドウを最背面に移動させるか、透明度を最低にします。
            - **引数**: なし。
            - **戻り値**: なし。
            - **機能**: 主にマウス接近時やフローモード時に、ユーザーの邪魔にならないようにウィンドウを目立たなくします。
        - `show_window()`:
            - **役割**: GUIウィンドウを最前面に表示させ、不透明度を元に戻します。
            - **引数**: なし。
            - **戻り値**: なし。
            - **機能**: ウィンドウが隠れた状態から、再びユーザーに見えるように表示を復元します。
- **main.py**:
    - `run_app(config_path: str = None)`:
        - **役割**: アプリケーションの主要な実行フローを管理します。
        - **引数**: `config_path` (str, オプション): カスタム設定ファイルのパス。
        - **戻り値**: なし。
        - **機能**: 設定を読み込み、`ScoreTracker`と`CatWindowWatcherGUI`のインスタンスを生成し、GUIのメインループを開始してアプリケーション全体を起動します。

## 関数呼び出し階層ツリー
```
run_app (src/main.py)
├── load_config (src/config.py)
├── ScoreTracker.__init__ (src/score_tracker.py)
├── CatWindowWatcherGUI.__init__ (src/gui.py)
│   └── (Tkinter GUIコンポーネントの初期化)
└── CatWindowWatcherGUI.start_periodic_update (src/gui.py)
    └── (繰り返し実行される内部コールバック関数)
        ├── get_active_window_title (src/window_monitor.py)
        ├── ScoreTracker.update_score (src/score_tracker.py)
        ├── ScoreTracker.is_score_decreasing (src/score_tracker.py)
        ├── ScoreTracker.is_flow_mode_active (src/score_tracker.py)
        ├── ScoreTracker.get_fade_opacity (src/score_tracker.py)
        ├── CatWindowWatcherGUI.update_display (src/gui.py)
        ├── (条件付き呼び出し) ScoreTracker.reset_score (src/score_tracker.py)
        ├── (条件付き呼び出し) CatWindowWatcherGUI.hide_window (src/gui.py)
        └── (条件付き呼び出し) CatWindowWatcherGUI.show_window (src/gui.py)

---
Generated at: 2026-01-02 07:06:08 JST
