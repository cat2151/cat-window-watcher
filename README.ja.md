# cat-window-watcher - Cat is watching you -

アクティブなウィンドウを監視し、あなたの作業内容に基づいてスコアを調整するシンプルでスタンドアロンなウィンドウ監視ツール。

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

開発中です。不具合があります。issueを参照ください

## ⚠️ 暫定実装についての注意

これは**テストと検証のための暫定実装**です。現在の実装は以下に焦点を当てています：
- シンプルでスタンドアロンな操作（この段階では他のアプリとの統合なし）
- 分かりやすいロジック：1秒ごとにアクティブなウィンドウタイトルをチェック
- 迅速な開発とテストを促進するための最小限の複雑さ

将来のバージョンでは最適化や統合が含まれる可能性がありますが、このバージョンはシンプルさと理解しやすさを優先しています。

## コンセプト

アプリケーションは現在アクティブなウィンドウを監視し、設定可能なパターンに基づいてスコアを調整します：
- GitHubで作業中？スコアが上がります！ 🎉
- SNSを閲覧中？スコアが下がります... 😿

The cat is watching you!

## 機能

- **シンプルなスコア表示**: クリーンなtkinter GUIで現在のスコアを表示
- **正規表現ベースのウィンドウマッチング**: 正規表現を使用してウィンドウタイトルパターンを設定
- **設定可能なスコア値**: 各パターンに対してカスタムなスコア増減量を設定
- **クロスプラットフォーム対応**: Linux、macOS、Windowsで動作
- **軽量**: 1秒に1回ウィンドウタイトルをチェック、最小限のリソース使用量

## 見た目

```
╔════════════════════════════════════════════════════════════╗
║   Cat Window Watcher - Cat is watching you -               ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║                                                            ║
║                       Score: 42                            ║
║                                                            ║
║                                                            ║
║                      GitHub (+10)                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

GUIはダークテーマで、大きなスコア表示と現在のアクティビティを表示するステータスを備えています。

## インストール

1. リポジトリをクローン：
```bash
git clone https://github.com/cat2151/cat-window-watcher.git
cd cat-window-watcher
```

2. Python 3.12以上がインストールされていることを確認：
```bash
python --version
```

3. 依存関係をインストール（必要に応じて）：
   - Linux: `xdotool` または `xprop`（通常はプリインストール済み）
   - macOS: 内蔵AppleScriptサポート
   - Windows: 内蔵APIで動作（より良いサポートのために `pywin32` をオプションで使用）

## 設定

1. 設定例をコピー：
```bash
cp config.toml.example config.toml
```

2. `config.toml`を編集してウィンドウパターンとスコアをカスタマイズ：

```toml
# デフォルトスコア（パターンがマッチしない場合に適用）
# 設定ミスを検知しやすくするために使用します
# -1（デフォルト）で設定ミスを簡単に検知、0に設定で無効化
default_score = -1

[[window_patterns]]
regex = "github"           # Regex pattern to match window title
score = 10                 # Score change when this window is active
description = "GitHub"     # Display description

[[window_patterns]]
regex = "twitter|x\\.com"
score = -5
description = "Twitter/X"
```

### 設定オプション

- **default_score**: パターンがマッチしない場合に適用されるスコア（デフォルト: -1）
  - -1（デフォルト）に設定すると、パターンが正しく設定されているか確認しやすくなります
  - 0に設定すると、マッチしない場合はスコアが変化しません
  - パターンが誤って設定されている場合、スコアが継続的に減少するため、すぐに気づくことができます
- **apply_default_score_mode**: デフォルトスコアの適用制御（デフォルト: true）
  - `true`（デフォルト）に設定すると、パターンがマッチしない場合に default_score が適用されます
  - `false`に設定すると、パターンがマッチしない場合でもスコアは変化しません（スコアは維持されます）
- **self_window_score**: アプリ自身のウィンドウがアクティブな場合に適用されるスコア（デフォルト: 0）
  - Cat Window Watcherのウィンドウ自体にフォーカスを切り替えた場合、default_scoreや「マッチなし」の代わりにこのスコアが適用されます
  - 0（デフォルト）に設定すると、アプリを確認している間はスコアが変化しません
  - 正の値に設定すると、スコアをチェックすることに報酬を与えます
  - 負の値に設定すると、過度なスコアチェックを抑制します
- **mild_penalty_mode**: 指定した時間帯にマイナススコアを -1 に制限するモード（デフォルト: false）
  - **注意**: これはテスト目的の暫定実装です
  - `true`に設定すると有効化、`false`で無効化（デフォルト: false）
- **mild_penalty_start_hour**: マイルドペナルティモードの開始時刻（0-23、デフォルト: 22）
  - mild_penalty_mode が有効な場合、mild_penalty_start_hour から mild_penalty_end_hour までの時間帯にマイナススコアが -1 に制限されます
- **mild_penalty_end_hour**: マイルドペナルティモードの終了時刻（0-23、デフォルト: 23）
  - 時間範囲は開始時刻と終了時刻の両方を含みます
- **always_on_top**: ウィンドウを常に最前面に表示するかどうか（デフォルト: true）
  - `true`に設定すると、ウィンドウが常に他のウィンドウの上に表示されます
  - `false`に設定すると、通常のウィンドウとして動作します
- **hide_on_mouse_proximity**: マウスが近づいたときにウィンドウを最背面に移動するかどうか（デフォルト: true）
  - `true`に設定すると、マウスカーソルがウィンドウに近づいたときに自動的に最背面に移動し、離れると最前面に戻ります
  - `false`に設定すると、この機能は無効になります
  - この機能は `always_on_top` が `true` の場合のみ動作します
- **proximity_distance**: マウス接近検知の距離（ピクセル単位、デフォルト: 50）
  - マウスカーソルがウィンドウからこの距離以内に入ったときに、ウィンドウを最背面に移動します
  - 値を大きくすると、より遠くからマウスを検知します
  - 値を小さくすると、ウィンドウにより近づかないと反応しません
- **always_on_top_while_score_decreasing**: スコアが減り続けている間、ウィンドウを最前面に表示（デフォルト: true）
  - `true`に設定すると、スコアが減少している間、ウィンドウを自動的に最前面に表示します
  - `false`に設定すると、この機能は無効になります
  - 集中力が低下している時（例：SNSを見ている時）に気づきやすくなります
  - スコアが減少している間は、他の最前面設定よりも優先されます
- **score_up_color**: スコアが上昇または変化しない場合の表示色（デフォルト: "#ffffff" 白）
  - スコアが増加したり、変化しない場合のフォント色を設定します
  - カラーコードは16進数形式（例: "#ffffff"）で指定します
- **score_down_color**: スコアが減少する場合の表示色（デフォルト: "#ff0000" 赤）
  - スコアが減少した場合のフォント色を設定します
  - カラーコードは16進数形式（例: "#ff0000"）で指定します
- **reset_score_every_30_minutes**: 30分ごとにスコアを0にリセットするかどうか（デフォルト: true）
  - `true`に設定すると、毎時00分と30分にスコアが自動的に0にリセットされます
  - `false`に設定すると、スコアは蓄積され続けます
  - ポモドーロ・テクニックに類似して、「今の30分だけ集中する」というイメージを作りやすくします
  - 例: 10:29にスコアが100でも、10:30になると0にリセットされ、新しい30分間が始まります
- **fade_window_on_flow_mode_enabled**: フロー状態の時にウィンドウを徐々に透明化するかどうか（デフォルト: false）
  - `true`に設定すると、スコア上昇状態が flow_mode_delay_seconds 続いた後、ウィンドウが徐々に透明化して集中を助けます
  - `false`に設定すると、この機能は無効になります
- **flow_mode_delay_seconds**: フェード開始前の待機時間（秒単位、デフォルト: 10）
  - 非スコア上昇状態からスコア上昇状態に移行した後、この秒数だけ待ってからフェード効果を開始します
- **flow_mode_fade_rate_percent_per_second**: フローモードの透明化速度（1秒あたりの透明度増加率、パーセント単位、デフォルト: 1）
  - フローモード中、ウィンドウは毎秒このパーセント分だけ透明になります
  - 範囲: 1-100（1 = ゆっくりとしたフェード、100 = 即座に透明化）
- **window_x / window_y**: ウィンドウの初期位置（X座標 / Y座標、ピクセル単位）
  - 両方が指定されている場合、ウィンドウはその位置に開きます
  - どちらか一方が指定されていない場合（または null に設定されている場合）は、システムがデフォルト位置を選択します
  - 座標は画面の左上隅を基準としたピクセル単位です
  - デフォルト: 未設定（null） - システムが位置を選択
- **copy_no_match_to_clipboard**: マッチしないウィンドウタイトルを自動的にクリップボードにコピーする（デフォルト: false）
  - `true`に設定すると、どのパターンにもマッチしないウィンドウタイトルが自動的にクリップボードにコピーされます
  - `false`に設定すると、この機能は無効になります
  - 新しいパターンの設定が簡単になります - ウィンドウに切り替えるだけでタイトルが取得でき、設定ファイルにペーストできます
  - 各ユニークなマッチしないタイトルは一度だけコピーされるため、繰り返しクリップボードが更新されることはありません
- **regex**: ウィンドウタイトルにマッチする正規表現パターン（大文字小文字を区別しない）
- **score**: パターンがマッチしたときにスコアに追加する整数値（負の値も可能）
- **description**: ステータスエリアに表示される人間が読める説明

## 使用法

アプリケーションを実行：
```bash
# 方法1: スクリプトを直接実行
python src/main.py

# 方法2: モジュールとして実行
python -m src

# 方法3: カスタム設定ファイルで実行
python src/main.py --config my_config.toml
python src/main.py -c my_config.toml
```

GUIには以下が表示されます：
- 現在のスコアを大きなテキストで表示
- 現在マッチしたパターンまたはウィンドウタイトルを表示するステータス
- 1秒ごとに自動更新

## 例

### 例1: 生産性の追跡
```toml
[[window_patterns]]
regex = "github|gitlab"
score = 10
description = "コーディング"

[[window_patterns]]
regex = "twitter|facebook|instagram"
score = -5
description = "ソーシャルメディア"
```

### 例2: 勉強時間
```toml
[[window_patterns]]
regex = "pdf|documentation|docs"
score = 8
description = "読書"

[[window_patterns]]
regex = "youtube|netflix"
score = -10
description = "エンターテイメント"
```

### 例3: 最前面モードでマウス接近時に自動で最背面に移動
```toml
# ウィンドウを常に最前面に表示しつつ、マウスが近づいたら自動的に最背面に移動
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
```

この設定により、ウィンドウは通常は最前面に表示されますが、マウスカーソルが50ピクセル以内に近づくと自動的に最背面に移動し、マウスが離れると再び最前面に戻ります。作業の邪魔にならないように設計されています。

## 開発

### テストの実行
```bash
python -m unittest discover tests/ -v
```

### コードフォーマット
コミット前にコードをフォーマット：
```bash
ruff format src/ tests/
ruff check --fix src/ tests/
```

### リンティング
コード品質の検証：
```bash
ruff format --check src/ tests/
ruff check src/ tests/
```

## アーキテクチャ

アプリケーションはいくつかのモジュールから構成されています：

- **config.py**: TOML設定の読み込みと管理
- **window_monitor.py**: クロスプラットフォームなウィンドウタイトル検出
- **score_tracker.py**: ウィンドウタイトルをパターンにマッチさせ、スコアを追跡
- **gui.py**: tkinterベースのスコア表示インターフェース
- **main.py**: アプリケーションのエントリポイントとオーケストレーション

## プラットフォーム固有の注意事項

### Linux
`xdotool` または `xprop` が必要：
```bash
sudo apt-get install xdotool  # Debian/Ubuntu
```

### macOS
内蔵AppleScriptを使用。追加の依存関係は不要。

### Windows
内蔵Windows APIで動作。より良い互換性のためにインストール：
```bash
pip install pywin32
```

## ライセンス

詳細はLICENSEファイルをご覧ください。

*Big Brother is watching you. But this time, it's a cat. 🐱*
