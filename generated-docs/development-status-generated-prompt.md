Last updated: 2026-01-10

# 開発状況生成プロンプト（開発者向け）

## 生成するもの：
- 現在openされているissuesを3行で要約する
- 次の一手の候補を3つlistする
- 次の一手の候補3つそれぞれについて、極力小さく分解して、その最初の小さな一歩を書く

## 生成しないもの：
- 「今日のissue目標」などuserに提案するもの
  - ハルシネーションの温床なので生成しない
- ハルシネーションしそうなものは生成しない（例、無価値なtaskや新issueを勝手に妄想してそれをuserに提案する等）
- プロジェクト構造情報（来訪者向け情報のため、別ファイルで管理）

## 「Agent実行プロンプト」生成ガイドライン：
「Agent実行プロンプト」作成時は以下の要素を必ず含めてください：

### 必須要素
1. **対象ファイル**: 分析/編集する具体的なファイルパス
2. **実行内容**: 具体的な分析や変更内容（「分析してください」ではなく「XXXファイルのYYY機能を分析し、ZZZの観点でmarkdown形式で出力してください」）
3. **確認事項**: 変更前に確認すべき依存関係や制約
4. **期待する出力**: markdown形式での結果や、具体的なファイル変更

### Agent実行プロンプト例

**良い例（上記「必須要素」4項目を含む具体的なプロンプト形式）**:
```
対象ファイル: `.github/workflows/translate-readme.yml`と`.github/workflows/call-translate-readme.yml`

実行内容: 対象ファイルについて、外部プロジェクトから利用する際に必要な設定項目を洗い出し、以下の観点から分析してください：
1) 必須入力パラメータ（target-branch等）
2) 必須シークレット（GEMINI_API_KEY）
3) ファイル配置の前提条件（README.ja.mdの存在）
4) 外部プロジェクトでの利用時に必要な追加設定

確認事項: 作業前に既存のworkflowファイルとの依存関係、および他のREADME関連ファイルとの整合性を確認してください。

期待する出力: 外部プロジェクトがこの`call-translate-readme.yml`を導入する際の手順書をmarkdown形式で生成してください。具体的には：必須パラメータの設定方法、シークレットの登録手順、前提条件の確認項目を含めてください。
```

**避けるべき例**:
- callgraphについて調べてください
- ワークフローを分析してください
- issue-noteの処理フローを確認してください

## 出力フォーマット：
以下のMarkdown形式で出力してください：

```markdown
# Development Status

## 現在のIssues
[以下の形式で3行でオープン中のissuesを要約。issue番号を必ず書く]
- [1行目の説明]
- [2行目の説明]
- [3行目の説明]

## 次の一手候補
1. [候補1のタイトル。issue番号を必ず書く]
   - 最初の小さな一歩: [具体的で実行可能な最初のアクション]
   - Agent実行プロンプト:
     ```
     対象ファイル: [分析/編集する具体的なファイルパス]

     実行内容: [具体的な分析や変更内容を記述]

     確認事項: [変更前に確認すべき依存関係や制約]

     期待する出力: [markdown形式での結果や、具体的なファイル変更の説明]
     ```

2. [候補2のタイトル。issue番号を必ず書く]
   - 最初の小さな一歩: [具体的で実行可能な最初のアクション]
   - Agent実行プロンプト:
     ```
     対象ファイル: [分析/編集する具体的なファイルパス]

     実行内容: [具体的な分析や変更内容を記述]

     確認事項: [変更前に確認すべき依存関係や制約]

     期待する出力: [markdown形式での結果や、具体的なファイル変更の説明]
     ```

3. [候補3のタイトル。issue番号を必ず書く]
   - 最初の小さな一歩: [具体的で実行可能な最初のアクション]
   - Agent実行プロンプト:
     ```
     対象ファイル: [分析/編集する具体的なファイルパス]

     実行内容: [具体的な分析や変更内容を記述]

     確認事項: [変更前に確認すべき依存関係や制約]

     期待する出力: [markdown形式での結果や、具体的なファイル変更の説明]
     ```
```


# 開発状況情報
- 以下の開発状況情報を参考にしてください。
- Issue番号を記載する際は、必ず [Issue #番号](../issue-notes/番号.md) の形式でMarkdownリンクとして記載してください。

## プロジェクトのファイル一覧
- .editorconfig
- .github/actions-tmp/.github/workflows/call-callgraph.yml
- .github/actions-tmp/.github/workflows/call-daily-project-summary.yml
- .github/actions-tmp/.github/workflows/call-issue-note.yml
- .github/actions-tmp/.github/workflows/call-rust-windows-check.yml
- .github/actions-tmp/.github/workflows/call-translate-readme.yml
- .github/actions-tmp/.github/workflows/callgraph.yml
- .github/actions-tmp/.github/workflows/check-recent-human-commit.yml
- .github/actions-tmp/.github/workflows/daily-project-summary.yml
- .github/actions-tmp/.github/workflows/issue-note.yml
- .github/actions-tmp/.github/workflows/rust-windows-check.yml
- .github/actions-tmp/.github/workflows/translate-readme.yml
- .github/actions-tmp/.github_automation/callgraph/codeql-queries/callgraph.ql
- .github/actions-tmp/.github_automation/callgraph/codeql-queries/codeql-pack.lock.yml
- .github/actions-tmp/.github_automation/callgraph/codeql-queries/qlpack.yml
- .github/actions-tmp/.github_automation/callgraph/config/example.json
- .github/actions-tmp/.github_automation/callgraph/docs/callgraph.md
- .github/actions-tmp/.github_automation/callgraph/presets/callgraph.js
- .github/actions-tmp/.github_automation/callgraph/presets/style.css
- .github/actions-tmp/.github_automation/callgraph/scripts/analyze-codeql.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/callgraph-utils.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/check-codeql-exists.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/check-node-version.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/common-utils.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/copy-commit-results.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/extract-sarif-info.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/find-process-results.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/generate-html-graph.cjs
- .github/actions-tmp/.github_automation/callgraph/scripts/generateHTML.cjs
- .github/actions-tmp/.github_automation/check_recent_human_commit/scripts/check-recent-human-commit.cjs
- .github/actions-tmp/.github_automation/project_summary/docs/daily-summary-setup.md
- .github/actions-tmp/.github_automation/project_summary/prompts/development-status-prompt.md
- .github/actions-tmp/.github_automation/project_summary/prompts/project-overview-prompt.md
- .github/actions-tmp/.github_automation/project_summary/scripts/ProjectSummaryCoordinator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/development/DevelopmentStatusGenerator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/development/GitUtils.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/development/IssueTracker.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/generate-project-summary.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/CodeAnalyzer.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/ProjectAnalysisOrchestrator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/ProjectDataCollector.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/ProjectDataFormatter.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/overview/ProjectOverviewGenerator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/shared/BaseGenerator.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/shared/FileSystemUtils.cjs
- .github/actions-tmp/.github_automation/project_summary/scripts/shared/ProjectFileUtils.cjs
- .github/actions-tmp/.github_automation/translate/docs/TRANSLATION_SETUP.md
- .github/actions-tmp/.github_automation/translate/scripts/translate-readme.cjs
- .github/actions-tmp/.gitignore
- .github/actions-tmp/.vscode/settings.json
- .github/actions-tmp/LICENSE
- .github/actions-tmp/README.ja.md
- .github/actions-tmp/README.md
- .github/actions-tmp/_config.yml
- .github/actions-tmp/generated-docs/callgraph.html
- .github/actions-tmp/generated-docs/callgraph.js
- .github/actions-tmp/generated-docs/development-status-generated-prompt.md
- .github/actions-tmp/generated-docs/development-status.md
- .github/actions-tmp/generated-docs/project-overview-generated-prompt.md
- .github/actions-tmp/generated-docs/project-overview.md
- .github/actions-tmp/generated-docs/style.css
- .github/actions-tmp/googled947dc864c270e07.html
- .github/actions-tmp/issue-notes/10.md
- .github/actions-tmp/issue-notes/11.md
- .github/actions-tmp/issue-notes/12.md
- .github/actions-tmp/issue-notes/13.md
- .github/actions-tmp/issue-notes/14.md
- .github/actions-tmp/issue-notes/15.md
- .github/actions-tmp/issue-notes/16.md
- .github/actions-tmp/issue-notes/17.md
- .github/actions-tmp/issue-notes/18.md
- .github/actions-tmp/issue-notes/19.md
- .github/actions-tmp/issue-notes/2.md
- .github/actions-tmp/issue-notes/20.md
- .github/actions-tmp/issue-notes/21.md
- .github/actions-tmp/issue-notes/22.md
- .github/actions-tmp/issue-notes/23.md
- .github/actions-tmp/issue-notes/24.md
- .github/actions-tmp/issue-notes/25.md
- .github/actions-tmp/issue-notes/26.md
- .github/actions-tmp/issue-notes/27.md
- .github/actions-tmp/issue-notes/28.md
- .github/actions-tmp/issue-notes/29.md
- .github/actions-tmp/issue-notes/3.md
- .github/actions-tmp/issue-notes/30.md
- .github/actions-tmp/issue-notes/4.md
- .github/actions-tmp/issue-notes/7.md
- .github/actions-tmp/issue-notes/8.md
- .github/actions-tmp/issue-notes/9.md
- .github/actions-tmp/package-lock.json
- .github/actions-tmp/package.json
- .github/actions-tmp/src/main.js
- .github/copilot-instructions.md
- .github/workflows/call-daily-project-summary.yml
- .github/workflows/call-issue-note.yml
- .github/workflows/call-translate-readme.yml
- .gitignore
- .pre-commit-config.yaml
- .vscode/settings.json
- LICENSE
- README.ja.md
- README.md
- _config.yml
- config.toml.example
- examples/example.txt
- generated-docs/project-overview-generated-prompt.md
- issue-notes/11.md
- issue-notes/12.md
- issue-notes/13.md
- issue-notes/14.md
- issue-notes/15.md
- issue-notes/16.md
- issue-notes/21.md
- issue-notes/26.md
- issue-notes/27.md
- issue-notes/29.md
- issue-notes/31.md
- issue-notes/33.md
- issue-notes/34.md
- issue-notes/37.md
- issue-notes/39.md
- issue-notes/4.md
- issue-notes/40.md
- issue-notes/43.md
- issue-notes/45.md
- issue-notes/46.md
- issue-notes/48.md
- issue-notes/50.md
- issue-notes/53.md
- issue-notes/55.md
- issue-notes/57.md
- issue-notes/58.md
- issue-notes/59.md
- issue-notes/6.md
- issue-notes/60.md
- issue-notes/61.md
- issue-notes/63.md
- issue-notes/65.md
- issue-notes/8.md
- issue-notes/9.md
- pytest.ini
- ruff.toml
- src/__init__.py
- src/__main__.py
- src/config.py
- src/config_loader.py
- src/config_validator.py
- src/constants.py
- src/flow_state_manager.py
- src/gui.py
- src/main.py
- src/score_calculator.py
- src/score_tracker.py
- src/status_formatter.py
- src/window_behavior.py
- src/window_monitor.py
- tests/test_config.py
- tests/test_dummy.py
- tests/test_gui.py
- tests/test_score_colors.py
- tests/test_score_tracker.py
- tests/test_screensaver_detection.py
- tests/test_window_monitor.py

## 現在のオープンIssues
## [Issue #60](../issue-notes/60.md): examplesのja版を生成する。README.ja.mdの説明も、そこを参照、とする
[issue-notes/60.md](https://github.com/cat2151/cat-window-watcher/blob/main/issue-notes/60.md)

...
ラベル: 
--- issue-notes/60.md の内容 ---

```markdown
# issue examplesのja版を生成する #60
[issues #60](https://github.com/cat2151/cat-window-watcher/issues/60)



```

## [Issue #59](../issue-notes/59.md): README.ja.mdの項目説明を読みやすくする。どれがwindow patterns内か、そうでないか、をパッと見でわかるようにする
[issue-notes/59.md](https://github.com/cat2151/cat-window-watcher/blob/main/issue-notes/59.md)

...
ラベル: 
--- issue-notes/59.md の内容 ---

```markdown
# issue README.ja.mdの項目説明を読みやすくする。どれがwindow patterns内か、そうでないか、をパッと見でわかるようにする #59
[issues #59](https://github.com/cat2151/cat-window-watcher/issues/59)



```

## [Issue #57](../issue-notes/57.md): examplesを読みやすくする。descriptionは要素の一番下でなく一番上にして、重複した内容のコメントを削除する
[issue-notes/57.md](https://github.com/cat2151/cat-window-watcher/blob/main/issue-notes/57.md)

...
ラベル: 
--- issue-notes/57.md の内容 ---

```markdown
# issue examplesを読みやすくする。descriptionは要素の一番下でなく一番上にして、重複した内容のコメントを削除する #57
[issues #57](https://github.com/cat2151/cat-window-watcher/issues/57)



```

## [Issue #26](../issue-notes/26.md): ドッグフーディングする
[issue-notes/26.md](https://github.com/cat2151/cat-window-watcher/blob/main/issue-notes/26.md)

...
ラベル: 
--- issue-notes/26.md の内容 ---

```markdown
# issue ドッグフーディングする #26
[issues #26](https://github.com/cat2151/cat-window-watcher/issues/26)



```

## ドキュメントで言及されているファイルの内容
### .github/actions-tmp/README.ja.md
```md
{% raw %}
# GitHub Actions 共通ワークフロー集

このリポジトリは、**複数プロジェクトで使い回せるGitHub Actions共通ワークフロー集**です

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

# 3行で説明
- 🚀 プロジェクトごとのGitHub Actions管理をもっと楽に
- 🔗 共通化されたワークフローで、どのプロジェクトからも呼ぶだけでOK
- ✅ メンテは一括、プロジェクト開発に集中できます

## Quick Links
| 項目 | リンク |
|------|--------|
| 📖 プロジェクト概要 | [generated-docs/project-overview.md](generated-docs/project-overview.md) |
| 📖 コールグラフ | [generated-docs/callgraph.html](https://cat2151.github.io/github-actions/generated-docs/callgraph.html) |
| 📊 開発状況 | [generated-docs/development-status.md](generated-docs/development-status.md) |

# notes
- まだ共通化の作業中です
- まだワークフロー内容を改善中です

※README.md は README.ja.md を元にGeminiの翻訳でGitHub Actionsで自動生成しています

{% endraw %}
```

### README.ja.md
```md
{% raw %}
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

- **verbose**: 設定の詳細を起動時に表示するかどうか（デフォルト: false）
  - `true`に設定すると、アプリケーション起動時に全ての設定値が表示されます
  - `false`に設定すると、設定の詳細は表示されません（デフォルト）
  - デバッグや設定の確認が必要な場合に有効にします
- **default_score**: パターンがマッチしない場合に適用されるスコア（デフォルト: -1）
  - -1（デフォルト）に設定すると、パターンが正しく設定されているか確認しやすくなります
  - 0に設定すると、マッチしない場合はスコアが変化しません
  - パターンが誤って設定されている場合、スコアが継続的に減少するため、すぐに気づくことができます
- **apply_default_score_mode**: デフォルトスコアの適用制御（デフォルト: true）
  - `true`に設定すると、パターンがマッチしない場合に default_score が適用されます
  - `false`に設定すると、パターンがマッチしない場合でもスコアは変化しません（スコアは維持されます）
- **self_window_score**: アプリ自身のウィンドウがアクティブな場合に適用されるスコア（デフォルト: 0）
  - Cat Window Watcherのウィンドウ自体にフォーカスを切り替えた場合、default_scoreや「マッチなし」の代わりにこのスコアが適用されます
  - 0（デフォルト）に設定すると、アプリを確認している間はスコアが変化しません
  - 正の値に設定すると、スコアをチェックすることに報酬を与えます
  - 負の値に設定すると、過度なスコアチェックを抑制します
- **mild_penalty_mode**: 指定した時間帯にマイナススコアを -1 に制限するモード（デフォルト: false）
  - **注意**: これはテスト目的の暫定実装です
  - `true`に設定すると有効化、`false`で無効化
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
- **default_transparency**: ウィンドウの初期透明度（デフォルト: 1.0）
  - ウィンドウ起動時の透明度/不透明度を設定します
  - 範囲: 0.0-1.0（0.0 = 完全に透明、1.0 = 完全に不透明）
  - デフォルトでウィンドウを少し透明にしたい場合に便利です
  - デフォルト: 1.0 - 完全に不透明
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

{% endraw %}
```

### .github/actions-tmp/issue-notes/26.md
```md
{% raw %}
# issue userによるcommitがなくなって24時間超経過しているのに、毎日ムダにproject summaryとcallgraphの自動生成が行われてしまっている #26
[issues #26](https://github.com/cat2151/github-actions/issues/26)

# どうする？
- logを確認する。24時間チェックがバグっている想定。
- もしlogから判別できない場合は、logを改善する。

# log確認結果
- botによるcommitなのに、user commitとして誤判別されている
```
Checking for user commits in the last 24 hours...
User commits found: true
Recent user commits:
7654bf7 Update callgraph.html [auto]
abd2f2d Update project summaries (overview & development status)
```

# ざっくり調査結果
- #27 が判明した

# どうする？
- [x] #27 を修正する。これで自動的に #26 も修正される想定。
    - 当該処理を修正する。
    - もしデータ不足なら、より詳細なlog生成を実装する。
- 別件として、このチェックはむしろworkflow ymlの先頭で行うのが適切と考える。なぜなら、以降のムダな処理をカットできるのでエコ。
    - [x] #28 を起票したので、そちらで実施する。

# close条件は？
- 前提
    - [x] 先行タスクである #27 と #28 が完了済みであること
- 誤爆がなくなること。
    - つまり、userによるcommitがなくなって24時間超経過後の日次バッチにて、
        - ムダなdevelopment status生成、等がないこと
        - jobのlogに「commitがないので処理しません」的なmessageが出ること
- どうする？
    - 日次バッチを本番を流して本番testする

# 結果
- github-actions logより：
    - 直近24hのcommitはbotによる1件のみであった
    - よって後続jobはskipとなった
    - ことを確認した
- close条件を満たした、と判断する
```
Run node .github_automation/check_recent_human_commit/scripts/check-recent-human-commit.cjs
BOT: Commit 5897f0c6df6bc2489f9ce3579b4f351754ee0551 | Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com> | Message: Update project summaries (overview & development status) [auto]
has_recent_human_commit=false
```

# closeとする

{% endraw %}
```

### issue-notes/26.md
```md
{% raw %}
# issue ドッグフーディングする #26
[issues #26](https://github.com/cat2151/cat-window-watcher/issues/26)



{% endraw %}
```

### .github/actions-tmp/issue-notes/7.md
```md
{% raw %}
# issue issue note生成できるかのtest用 #7
[issues #7](https://github.com/cat2151/github-actions/issues/7)

- 生成できた
- closeとする

{% endraw %}
```

### .github/actions-tmp/issue-notes/9.md
```md
{% raw %}
# issue 関数コールグラフhtmlビジュアライズが0件なので、原因を可視化する #9
[issues #9](https://github.com/cat2151/github-actions/issues/9)

# agentに修正させたり、人力で修正したりした
- agentがハルシネーションし、いろいろ根の深いバグにつながる、エラー隠蔽などを仕込んでいたため、検知が遅れた
- 詳しくはcommit logを参照のこと
- WSL + actの環境を少し変更、act起動時のコマンドライン引数を変更し、generated-docsをmountする（ほかはデフォルト挙動であるcpだけにする）ことで、デバッグ情報をコンテナ外に出力できるようにし、デバッグを効率化した

# test green

# closeとする

{% endraw %}
```

### issue-notes/9.md
```md
{% raw %}
# issue マッチしない場合のscore、を定義し、マッチ設定ミスを検知しやすくする #9
[issues #9](https://github.com/cat2151/cat-window-watcher/issues/9)



{% endraw %}
```

### issue-notes/57.md
```md
{% raw %}
# issue examplesを読みやすくする。descriptionは要素の一番下でなく一番上にして、重複した内容のコメントを削除する #57
[issues #57](https://github.com/cat2151/cat-window-watcher/issues/57)



{% endraw %}
```

### issue-notes/59.md
```md
{% raw %}
# issue README.ja.mdの項目説明を読みやすくする。どれがwindow patterns内か、そうでないか、をパッと見でわかるようにする #59
[issues #59](https://github.com/cat2151/cat-window-watcher/issues/59)



{% endraw %}
```

### issue-notes/6.md
```md
{% raw %}
# issue config.toml.example のgithubについて、githubのサイトを閲覧していても、ウィンドウタイトルにgithubを含まないPull requestsやCodeでgithubサイトと認識されない #6
[issues #6](https://github.com/cat2151/cat-window-watcher/issues/6)



{% endraw %}
```

### issue-notes/60.md
```md
{% raw %}
# issue examplesのja版を生成する #60
[issues #60](https://github.com/cat2151/cat-window-watcher/issues/60)



{% endraw %}
```

## 最近の変更（過去7日間）
### コミット履歴:
9585d19 Merge pull request #67 from cat2151/copilot/set-default-score-to-plus-one
15fc1da Change default score for window_patterns from 0 to +1
c020078 Initial plan
99add34 Update project summaries (overview & development status) [auto]
6763c29 Merge pull request #66 from cat2151/copilot/refactor-large-code-base
3e0f959 Fix validation issues: add missing validations and prevent boolean/integer type confusion
0478440 Phase 3: Refactor score_tracker.py - split into score_calculator and flow_state_manager modules
5253e76 Phase 2: Refactor gui.py - split into status_formatter and window_behavior modules
c2033bb Phase 1: Refactor config.py - split into validator and loader modules
46fde74 Initial plan

### 変更されたファイル:
config.toml.example
generated-docs/development-status-generated-prompt.md
generated-docs/development-status.md
generated-docs/project-overview-generated-prompt.md
generated-docs/project-overview.md
issue-notes/63.md
issue-notes/65.md
src/config.py
src/config_loader.py
src/config_validator.py
src/flow_state_manager.py
src/gui.py
src/score_calculator.py
src/score_tracker.py
src/status_formatter.py
src/window_behavior.py
src/window_monitor.py
tests/test_config.py
tests/test_screensaver_detection.py


---
Generated at: 2026-01-10 07:05:55 JST
