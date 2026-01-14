Last updated: 2026-01-15

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
- examples/README.ja.md
- examples/README.md
- examples/example1_productivity.ja.toml
- examples/example1_productivity.toml
- examples/example2_study_time.ja.toml
- examples/example2_study_time.toml
- examples/example3_always_on_top.ja.toml
- examples/example3_always_on_top.toml
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
- issue-notes/73.md
- issue-notes/75.md
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
## [Issue #75](../issue-notes/75.md): PR 74 を参考に、スクリーンセーバー認識がなぜ失敗しているか調査を進める
[issue-notes/75.md](https://github.com/cat2151/cat-window-watcher/blob/main/issue-notes/75.md)

...
ラベル: 
--- issue-notes/75.md の内容 ---

```markdown
# issue PR 74 を参考に、スクリーンセーバー認識がなぜ失敗しているか調査を進める #75
[issues #75](https://github.com/cat2151/cat-window-watcher/issues/75)



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

### issue-notes/6.md
```md
{% raw %}
# issue config.toml.example のgithubについて、githubのサイトを閲覧していても、ウィンドウタイトルにgithubを含まないPull requestsやCodeでgithubサイトと認識されない #6
[issues #6](https://github.com/cat2151/cat-window-watcher/issues/6)



{% endraw %}
```

### issue-notes/75.md
```md
{% raw %}
# issue PR 74 を参考に、スクリーンセーバー認識がなぜ失敗しているか調査を進める #75
[issues #75](https://github.com/cat2151/cat-window-watcher/issues/75)



{% endraw %}
```

## 最近の変更（過去7日間）
### コミット履歴:
8825b41 Add issue note for #75 [auto]
17617a5 Merge pull request #74 from cat2151/copilot/add-screensaver-status-print
1e3a0a4 Add debug_screensaver_detection configuration option
162fe5f Initial plan
de6a7c9 Add issue note for #73 [auto]
a6f8d41 Update project summaries (overview & development status) [auto]
9d14e1e Auto-translate README.ja.md to README.md [auto]
ccc615a Merge pull request #72 from cat2151/copilot/add-ja-version-examples
f34f950 Reorder default_score before window settings in example3 for consistency
ab3f260 Add README files for examples directory in both English and Japanese

### 変更されたファイル:
README.ja.md
README.md
config.toml.example
examples/README.ja.md
examples/README.md
examples/example.txt
examples/example1_productivity.ja.toml
examples/example1_productivity.toml
examples/example2_study_time.ja.toml
examples/example2_study_time.toml
examples/example3_always_on_top.ja.toml
examples/example3_always_on_top.toml
generated-docs/development-status-generated-prompt.md
generated-docs/development-status.md
generated-docs/project-overview-generated-prompt.md
generated-docs/project-overview.md
issue-notes/73.md
issue-notes/75.md
src/config.py
src/config_loader.py
src/gui.py
src/window_monitor.py
tests/test_config.py


---
Generated at: 2026-01-15 07:05:55 JST
