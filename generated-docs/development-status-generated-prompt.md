Last updated: 2025-12-29

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
- issue-notes/4.md
- issue-notes/6.md
- issue-notes/8.md
- issue-notes/9.md
- pytest.ini
- ruff.toml
- src/__init__.py
- src/__main__.py
- src/config.py
- src/gui.py
- src/main.py
- src/score_tracker.py
- src/window_monitor.py
- tests/test_config.py
- tests/test_dummy.py
- tests/test_gui.py
- tests/test_score_tracker.py
- tests/test_window_monitor.py

## 現在のオープンIssues
## [Issue #23](../issue-notes/23.md): Add configurable score colors for increase/decrease states
Issue #13 requests making the score font color configurable, particularly displaying red when score decreases.

## Changes

**Configuration (`config.py`, `config.toml.example`)**
- Added `score_up_color` (default: `#ffffff`) and `score_down_color` (default: `#ff0000`) TOML settings
- Implemented hex...
ラベル: 
--- issue-notes/23.md の内容 ---

```markdown

```

## [Issue #16](../issue-notes/16.md): ポモドーロ・テクニックに類似して、今の30分だけ集中、をイメージしやすくするよう、時報の30分区切りごとにスコアを0リセット、をtomlでon/off可能にする
[issue-notes/16.md](https://github.com/cat2151/cat-window-watcher/blob/main/issue-notes/16.md)

...
ラベル: 
--- issue-notes/16.md の内容 ---

```markdown
# issue ポモドーロ・テクニックに類似して、今の30分だけ集中、をイメージしやすくするよう、時報の30分区切りごとにスコアを0リセット、をtomlでon/off可能にする #16
[issues #16](https://github.com/cat2151/cat-window-watcher/issues/16)



```

## [Issue #14](../issue-notes/14.md): 非score upからscore upに転じて10秒経過したら、userのフロー状態への没入をサポートするよう、ウィンドウ全体を1秒ごとに1%ずつ透明に近づける、というモードをtomlでon/off可能にする
[issue-notes/14.md](https://github.com/cat2151/cat-window-watcher/blob/main/issue-notes/14.md)

...
ラベル: 
--- issue-notes/14.md の内容 ---

```markdown
# issue 非score upからscore upに転じて10秒経過したら、userのフロー状態への没入をサポートするよう、ウィンドウ全体を1秒ごとに1%ずつ透明に近づける、というモードをtomlでon/off可能にする #14
[issues #14](https://github.com/cat2151/cat-window-watcher/issues/14)



```

## [Issue #13](../issue-notes/13.md): scoreが減少するときは、scoreを赤い文字にする、をtomlで実現可能にする。例えばfont colorをscore upとscore downで個別設定可能とする
[issue-notes/13.md](https://github.com/cat2151/cat-window-watcher/blob/main/issue-notes/13.md)

...
ラベル: 
--- issue-notes/13.md の内容 ---

```markdown
# issue scoreが減少するときは、scoreを赤い文字にする、をtomlで実現可能にする。例えばfont colorをscore upとscore downで個別設定可能とする #13
[issues #13](https://github.com/cat2151/cat-window-watcher/issues/13)



```

## ドキュメントで言及されているファイルの内容
### .github/actions-tmp/issue-notes/13.md
```md
{% raw %}
# issue issue-note を他projectから使いやすくする #13
[issues #13](https://github.com/cat2151/github-actions/issues/13)

- docs
    - call導入手順を書く

{% endraw %}
```

### issue-notes/13.md
```md
{% raw %}
# issue scoreが減少するときは、scoreを赤い文字にする、をtomlで実現可能にする。例えばfont colorをscore upとscore downで個別設定可能とする #13
[issues #13](https://github.com/cat2151/cat-window-watcher/issues/13)



{% endraw %}
```

### .github/actions-tmp/issue-notes/14.md
```md
{% raw %}
# issue Development Status のdocument生成において、最初の小さな一歩 を実現する用のプロンプト生成がされなくなっている #14
[issues #14](https://github.com/cat2151/github-actions/issues/14)

## 何が困るの？
- #11の場合
- 期待値
    - 最初の小さな一歩 : [Issue #11]のtranslateについて、現在の処理フローを確認し、外部プロジェクトから利用する際にどのような情報（翻訳対象のファイルパス、ターゲット言語設定など）が必要となるかを明確にする。これにより、再利用可能なワークフロー設計の基礎を築く。
    - 最初の小さな一歩をagentに実行させるためのプロンプト : 現在のGitHub Actions翻訳ワークフロー（translate-readme.yml、call-translate-readme.yml、translate-readme.cjs）を分析し、外部プロジェクトから利用する際に必要となる設定項目を洗い出してください。具体的には、以下の観点から調査し、markdown形式でまとめてください：1) 必須入力パラメータ（現在はtarget-branchのみ） 2) 必須シークレット（GEMINI_API_KEY） 3) ファイル配置の前提条件（README.ja.md の存在、配置場所） 4) 翻訳対象ファイル名の制約（現在はREADME固定） 5) ブランチ・トリガー設定の制約 6) 外部プロジェクトでの利用時に追加で必要となりそうな設定項目の提案
- 実際の結果
    - 最初の小さな一歩: [Issue #11]のtranslateについて、現在の処理フローを確認し、外部プロジェクトから利用する際にどのような情報（翻訳対象のファイルパス、ターゲット言語設定など）が必要となるかを明確にする。これにより、再利用可能なワークフロー設計の基礎を築く。

## close条件
- 期待値のように、Agent実行プロンプト、が生成されること

## agentに修正させた
- development-status.md を修正させた
- test green

## closeとする

{% endraw %}
```

### issue-notes/14.md
```md
{% raw %}
# issue 非score upからscore upに転じて10秒経過したら、userのフロー状態への没入をサポートするよう、ウィンドウ全体を1秒ごとに1%ずつ透明に近づける、というモードをtomlでon/off可能にする #14
[issues #14](https://github.com/cat2151/cat-window-watcher/issues/14)



{% endraw %}
```

### .github/actions-tmp/issue-notes/16.md
```md
{% raw %}
# issue issue-note / project-summary / translate / callgraph をtonejs-mml-to-jsonから呼び出す #16
[issues #16](https://github.com/cat2151/github-actions/issues/16)

# これまでの課題
- issue-note / project-summary / translate / callgraph は、github-actions リポジトリ上ではtest greenである。
- だが他のリポジトリにおいて動作するか？が可視化不足である。

# 対策
- issue-note / project-summary / translate / callgraph をtonejs-mml-to-jsonから呼び出す
- 詳しく
    - まず、現状、tonejs-mml-to-json でその4つのworkflowがどうなっているか、このmdに可視化する
    - 例えば、既に呼び出している、呼び出していない、tonejs-mml-to-jsonにある古いworkflowを呼び出している

# 調査結果
- まず、現状、tonejs-mml-to-json でその4つのworkflowがどうなっているか、このmdに可視化する
    - 結果：
        - issue-note
            - tonejs-mml-to-jsonにある古いworkflowを呼び出している
        - project-summary
            - tonejs-mml-to-jsonにある古いworkflowを呼び出している
        - translate
            - tonejs-mml-to-jsonにある古いworkflowを呼び出している
        - callgraph
            - tonejs-mml-to-jsonにある古いworkflowを呼び出している

# どうする？
- issue-note
    - github-actions リポジトリにある、call-issue-note.yml をcpして使うようにする、まず単純cpして動くかを確認する
- project-summary
    - github-actions リポジトリにある、call-daily-project-summary.yml をcpして使うようにする、まず単純cpして動くかを確認する
- translate
    - github-actions リポジトリにある、call-translate-readme.yml をcpして使うようにする、まず単純cpして動くかを確認する
- callgraph
    - github-actions リポジトリにある、call-callgraph.yml をcpして使うようにする、まず単純cpして動くかを確認する

# 状況
- issue-note
    - tonejs-mml-to-jsonリポジトリにて、test green
    - issue-noteについては当issueのタスクは完了した、と判断する
- project-summary
    - tonejs-mml-to-jsonリポジトリにて、test green
    - project-summaryについては当issueのタスクは完了した、と判断する

# 状況
- translate
    - github-actions リポジトリにある、call-translate-readme.yml をcpして使うようにする、まず単純cpして動くかを確認する
        - 状況
            - 単純cpした
            - ソース机上レビューした。OK
            - トリガーはREADME.ja.mdのcommit
            - testは省略とする
            - もし今後README.ja.mdのcommit時にうまく動作しないとしても、そのとき対処すればOK、と判断する
    - translateについては当issueのタスクは完了した、と判断する

# どうする？
- callgraph
    - github-actions リポジトリにある、call-callgraph.yml をcpして使うようにする、まず単純cpして動くかを確認する

# 結果
- callgraph
    - tonejs-mml-to-jsonリポジトリにて、test red
    - logをみても情報不足なため、まずloggerを修正する
    - 結果、わかった、運用ミス、対象srcの指定の考慮漏れ
    - どうする？
        - 対象srcを指定する。tonejs-mml-to-jsonリポジトリにて進める
    - 結果
        - test green
    - callgraphについては当issueのタスクは完了した、と判断する

# 状況
- github-actions以外のリポジトリとして、
    - tonejs-mml-to-jsonリポジトリにおいて、
        - issue-note / project-summary / translate / callgraph がtest greenとなった。
        - closeできる、と判断する。

# closeとする

{% endraw %}
```

### issue-notes/16.md
```md
{% raw %}
# issue ポモドーロ・テクニックに類似して、今の30分だけ集中、をイメージしやすくするよう、時報の30分区切りごとにスコアを0リセット、をtomlでon/off可能にする #16
[issues #16](https://github.com/cat2151/cat-window-watcher/issues/16)



{% endraw %}
```

### .github/actions-tmp/issue-notes/23.md
```md
{% raw %}
# issue issue 17が再発してしまっている #23
[issues #23](https://github.com/cat2151/github-actions/issues/23)

# 症状は？
- issue 17と同じ

# どうする？
- development-status-generated-prompt.md を確認する
- 結果
    - >Issue番号を記載する際は、必ず [Issue #番号](issue-notes/番号.md) の形式でMarkdownリンクとして記載してください。
    - 仮説、これが残っており、ほかの ../ 指定と競合し、どちらかがランダムで選ばれていた
    - 対策、ここを ../ 指定にする

# 結果
- test green

# closeとする

{% endraw %}
```

### .github/actions-tmp/issue-notes/3.md
```md
{% raw %}
# issue GitHub Actions「issue note生成」を共通ワークフロー化する #3
[issues #3](https://github.com/cat2151/github-actions/issues/3)

- 前提
  - userは、translateのworkflowを共通ワークフロー化し、動くようにしたので、共通ワークフロー化の知識がある
  - よって、今回は、promptでplanさせ、そのplanをuserがレビューし、planの改善を指示できるので、ハルシネーションのリスクを下げることができる

- prompt
```
あなたはGitHub Actionsと共通ワークフローのスペシャリストです。
このymlはまだ共通ワークフロー化されず、
呼び出し元からコピーされたままの状態です。
このymlファイル名のまま、
中身を共通ワークフロー化してください。
呼び出し元ymlは別途書きますので気にしないでください。
まずplanしてください
```

- plan 生成結果
```
共通ワークフロー化のためのplanは以下の通りです。

1. 目的
現在の issue-note.yml を「共通ワークフロー」として再設計し、他リポジトリや他ワークフローから workflow_call で呼び出せるようにする。
2. 主な変更点
on: トリガーを workflow_call に変更（直接イベントで起動しない）。
必要な入力（inputs）やシークレット（secrets）を workflow_call セクションで定義。
github.event.issue などのイベント依存部分を、inputs経由で受け取る形に修正。
既存の処理（issueノート生成、コミット、issue body更新）はそのまま活かすが、パラメータ化する。
3. 具体的な修正内容
on: issues: → on: workflow_call: に変更。
inputs で必要な値（例: issue_title, issue_number, issue_body, issue_url など）を受け取る。
スクリプト内の ${{ github.event.issue.xxx }} を ${{ inputs.xxx }} に置換。
github-script ステップも同様にinputsを参照。
必要に応じて secrets も workflow_call で受け取れるようにする。
4. ファイル名・配置
ファイル名はそのまま issue-note.yml。
配置場所は workflows でOK（共通ワークフローとしてもこの場所で良い）。
5. 呼び出し元への影響
呼び出し元ワークフローで uses: <repo>/.github/workflows/issue-note.yml@main のように参照し、inputsを渡す形になる。
このplanで進めます。次に、実際の共通ワークフロー化のためのyml修正案を作成しますか？
```

- userがplanレビューし、OKを出した
- agentに生成結果ymlをレビューさせた、OKとなった
  - userはこのレビューは認知負荷が高いのでskipとする（単純な細かい間違い探し作業になるので、それはagentに任せた）
-  エラー。呼び出し元ymlのエラーがあり修正。共通ワークフローのエラー指摘があり、共通ワークフロー側の修正が必要となった
```
原因の分析：

呼び出し元（tonejs-mml-to-jsonのissue-note.yml）は、reusable workflow（cat2151/github-actions/.github/workflows/issue-note.yml@main）をusesで呼び出し、inputsをwithで渡しています。
共通ワークフロー（reusable workflow）は inputs を workflow_call で受け取り、各ステップで ${{ inputs.xxx }} で参照しています。
しかし、エラーが発生したのは actions/github-script@v7 の script 内です。
エラーの本質的な原因：

actions/github-script の script: で ${{ inputs.issue_number }} のような式を直接 JavaScript テンプレートリテラル内で使っていますが、これはサポートされていません。
script: の中は JavaScript であり、YAMLの ${{ ... }} は展開されません（または意図通りに展開されません）。
そのため、inputs 変数は script 内の JavaScript で未定義となり、ReferenceError になります。
正しい書き方：

actions/github-script の script: でワークフローの inputs を使いたい場合は、with: で input を environment 変数や script の引数として渡し、JavaScript で process.env から取得するか、github-script の input 機能を使う必要があります。
例（修正版）：

このように、inputs の値を env で渡し、script 内では process.env で参照してください。

まとめ：

actions/github-script の script 内で ${{ inputs.xxx }} を直接使うと ReferenceError になる
env: で値を渡し、process.env で参照するのが正しい
修正が必要です。修正版のワークフローが必要な場合はお知らせください。
```

- test green
- closeとする

{% endraw %}
```

### .github/actions-tmp/issue-notes/4.md
```md
{% raw %}
# issue GitHub Actions「project概要生成」を共通ワークフロー化する #4
[issues #4](https://github.com/cat2151/github-actions/issues/4)

# prompt
```
あなたはGitHub Actionsと共通ワークフローのスペシャリストです。
このymlファイルを、以下の2つのファイルに分割してください。
1. 共通ワークフロー       cat2151/github-actions/.github/workflows/daily-project-summary.yml
2. 呼び出し元ワークフロー cat2151/github-actions/.github/workflows/call-daily-project-summary.yml
まずplanしてください
```

# 結果、あちこちハルシネーションのあるymlが生成された
- agentの挙動があからさまにハルシネーション
    - インデントが修正できない、「失敗した」という
    - 構文誤りを認識できない
- 人力で修正した

# このagentによるセルフレビューが信頼できないため、別のLLMによるセカンドオピニオンを試す
```
あなたはGitHub Actionsと共通ワークフローのスペシャリストです。
以下の2つのファイルをレビューしてください。最優先で、エラーが発生するかどうかだけレビューてください。エラー以外の改善事項のチェックをするかわりに、エラー発生有無チェックに最大限注力してください。

--- 呼び出し元

name: Call Daily Project Summary

on:
  schedule:
    # 日本時間 07:00 (UTC 22:00 前日)
    - cron: '0 22 * * *'
  workflow_dispatch:

jobs:
  call-daily-project-summary:
    uses: cat2151/github-actions/.github/workflows/daily-project-summary.yml
    secrets:
      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}

--- 共通ワークフロー
name: Daily Project Summary
on:
  workflow_call:

jobs:
  generate-summary:
    runs-on: ubuntu-latest

    permissions:
      contents: write
      issues: read
      pull-requests: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0  # 履歴を取得するため

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          # 一時的なディレクトリで依存関係をインストール
          mkdir -p /tmp/summary-deps
          cd /tmp/summary-deps
          npm init -y
          npm install @google/generative-ai @octokit/rest
          # generated-docsディレクトリを作成
          mkdir -p $GITHUB_WORKSPACE/generated-docs

      - name: Generate project summary
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          NODE_PATH: /tmp/summary-deps/node_modules
        run: |
          node .github/scripts/generate-project-summary.cjs

      - name: Check for generated summaries
        id: check_summaries
        run: |
          if [ -f "generated-docs/project-overview.md" ] && [ -f "generated-docs/development-status.md" ]; then
            echo "summaries_generated=true" >> $GITHUB_OUTPUT
          else
            echo "summaries_generated=false" >> $GITHUB_OUTPUT
          fi

      - name: Commit and push summaries
        if: steps.check_summaries.outputs.summaries_generated == 'true'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          # package.jsonの変更のみリセット（generated-docsは保持）
          git restore package.json 2>/dev/null || true
          # サマリーファイルのみを追加
          git add generated-docs/project-overview.md
          git add generated-docs/development-status.md
          git commit -m "Update project summaries (overview & development status)"
          git push

      - name: Summary generation result
        run: |
          if [ "${{ steps.check_summaries.outputs.summaries_generated }}" == "true" ]; then
            echo "✅ Project summaries updated successfully"
            echo "📊 Generated: project-overview.md & development-status.md"
          else
            echo "ℹ️ No summaries generated (likely no user commits in the last 24 hours)"
          fi
```

# 上記promptで、2つのLLMにレビューさせ、合格した

# 細部を、先行する2つのymlを参照に手直しした

# ローカルtestをしてからcommitできるとよい。方法を検討する
- ローカルtestのメリット
    - 素早く修正のサイクルをまわせる
    - ムダにgit historyを汚さない
        - これまでの事例：「実装したつもり」「エラー。修正したつもり」「エラー。修正したつもり」...（以降エラー多数）
- 方法
    - ※検討、WSL + act を環境構築済みである。test可能であると判断する
    - 呼び出し元のURLをコメントアウトし、相対パス記述にする
    - ※備考、テスト成功すると結果がcommit pushされる。それでよしとする
- 結果
    - OK
    - secretsを簡略化できるか試した、できなかった、現状のsecrets記述が今わかっている範囲でベストと判断する
    - OK

# test green

# commit用に、yml 呼び出し元 uses をlocal用から本番用に書き換える

# closeとする

{% endraw %}
```

### issue-notes/4.md
```md
{% raw %}
# issue GitHubを開いているあいだ1秒ごとにscoreが増える設定にしているが、増えない #4
[issues #4](https://github.com/cat2151/cat-window-watcher/issues/4)



{% endraw %}
```

### config.toml.example
```example
{% raw %}
# Cat Window Watcher Configuration
# This is a provisional implementation for testing purposes

# Default score applied when no window pattern matches
# This helps detect configuration errors - if patterns are misconfigured,
# you'll see this score being applied repeatedly
# Set to -1 (default) to easily spot misconfigurations, or 0 to disable
default_score = -1

# Apply default score mode - control whether default_score is applied
# This is a mode to enable/disable the application of default_score
# Set to true (default) to apply default_score when no pattern matches
# Set to false to not apply any score when no pattern matches (score stays unchanged)
apply_default_score_mode = true

# Mild penalty mode - limit negative scores to -1 during specified hours
# This is a provisional implementation for testing purposes
# Set to true to enable, false to disable (default: false)
mild_penalty_mode = false

# Start hour for mild penalty mode (0-23, default: 22)
# When mild_penalty_mode is enabled, negative scores will be limited to -1
# during the time range from mild_penalty_start_hour to mild_penalty_end_hour
mild_penalty_start_hour = 22

# End hour for mild penalty mode (0-23, default: 23)
# The time range is inclusive of both start and end hours
mild_penalty_end_hour = 23

# Always on top mode - keep the window on top of all other windows
# Set to true to enable, false to disable (default: false)
always_on_top = false

# Hide on mouse proximity mode - when always_on_top is enabled,
# hide the window (move to background) when mouse cursor approaches it
# Set to true to enable, false to disable (default: false)
# This only works when always_on_top is true
hide_on_mouse_proximity = false

# Proximity distance in pixels - distance threshold for mouse proximity detection
# When mouse cursor is within this distance from the window, it will be hidden
# Default: 50 pixels
proximity_distance = 50

# Window patterns define regex patterns to match window titles
# and the score change when that window becomes active

[[window_patterns]]
# GitHub - increases score when working on GitHub
# Matches both embedded "github" (e.g., "github.com", "GitHub - Profile")
# and GitHub pages format (e.g., "Pull requests · owner/repo · GitHub")
regex = "github|· GitHub$"
score = 10
description = "GitHub"

[[window_patterns]]
# Twitter/X - decreases score when browsing social media
regex = 'twitter|x\.com'
score = -5
description = "Twitter/X"

[[window_patterns]]
# Facebook - decreases score when browsing social media
regex = "facebook"
score = -5
description = "Facebook"

[[window_patterns]]
# Instagram - decreases score when browsing social media
regex = "instagram"
score = -5
description = "Instagram"

[[window_patterns]]
# Reddit - decreases score when browsing social media
regex = "reddit"
score = -3
description = "Reddit"

[[window_patterns]]
# Visual Studio Code - increases score when coding
regex = "visual studio code|vscode"
score = 8
description = "VS Code"

[[window_patterns]]
# Terminal - increases score when using terminal
regex = "terminal|bash|zsh|powershell"
score = 5
description = "Terminal"

[[window_patterns]]
# YouTube - decreases score when watching videos
regex = "youtube"
score = -7
description = "YouTube"

{% endraw %}
```

### issue-notes/6.md
```md
{% raw %}
# issue config.toml.example のgithubについて、githubのサイトを閲覧していても、ウィンドウタイトルにgithubを含まないPull requestsやCodeでgithubサイトと認識されない #6
[issues #6](https://github.com/cat2151/cat-window-watcher/issues/6)



{% endraw %}
```

### src/config.py
```py
{% raw %}
#!/usr/bin/env python3
"""Configuration module for cat-window-watcher."""

import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


class Config:
    """Configuration manager for window watcher."""

    def __init__(self, config_path: str = "config.toml"):
        """Initialize configuration.

        Args:
            config_path: Path to TOML configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
            tomllib.TOMLDecodeError: If config file is invalid
        """
        self.config_path = Path(config_path)
        self.window_patterns = []
        self.default_score = -1
        self.apply_default_score_mode = True
        self.always_on_top = False
        self.hide_on_mouse_proximity = False
        self.proximity_distance = 50
        self.mild_penalty_mode = False
        self.mild_penalty_start_hour = 22
        self.mild_penalty_end_hour = 23
        self._last_modified = None
        self.load_config()

    def load_config(self, exit_on_error=True):
        """Load configuration from TOML file.

        Args:
            exit_on_error: If True, exit on error. If False, raise exception.

        Raises:
            FileNotFoundError: If config file doesn't exist
            tomllib.TOMLDecodeError: If config file is invalid
            Exception: If other errors occur during loading
        """
        try:
            with open(self.config_path, "rb") as f:
                config_data = tomllib.load(f)

            # Load default_score (score applied when no pattern matches)
            default_score = config_data.get("default_score", -1)

            # Load apply_default_score_mode setting (whether to apply default score)
            apply_default_score_mode = config_data.get("apply_default_score_mode", True)
            if not isinstance(apply_default_score_mode, bool):
                raise ValueError(
                    f"Invalid 'apply_default_score_mode' value: {apply_default_score_mode!r}. Must be a boolean."
                )

            # Load always_on_top setting (whether window should stay on top)
            always_on_top = config_data.get("always_on_top", False)

            # Load hide_on_mouse_proximity setting (hide window when mouse is near)
            hide_on_mouse_proximity = config_data.get("hide_on_mouse_proximity", False)

            # Load proximity_distance setting (distance in pixels)
            # Ensure it is a non-negative integer; raise error if invalid
            proximity_distance = config_data.get("proximity_distance", 50)
            if not isinstance(proximity_distance, int) or proximity_distance < 0:
                raise ValueError(
                    f"Invalid 'proximity_distance' value: {proximity_distance!r}. Must be a non-negative integer."
                )

            # Load mild_penalty_mode setting (whether to apply mild penalty during specified hours)
            mild_penalty_mode = config_data.get("mild_penalty_mode", False)
            if not isinstance(mild_penalty_mode, bool):
                raise ValueError(f"Invalid 'mild_penalty_mode' value: {mild_penalty_mode!r}. Must be a boolean.")

            # Load mild_penalty_start_hour setting (start hour for mild penalty, default: 22)
            mild_penalty_start_hour = config_data.get("mild_penalty_start_hour", 22)
            if not isinstance(mild_penalty_start_hour, int) or not (0 <= mild_penalty_start_hour <= 23):
                raise ValueError(
                    f"Invalid 'mild_penalty_start_hour' value: {mild_penalty_start_hour!r}. Must be an integer between 0 and 23."
                )

            # Load mild_penalty_end_hour setting (end hour for mild penalty, default: 23)
            mild_penalty_end_hour = config_data.get("mild_penalty_end_hour", 23)
            if not isinstance(mild_penalty_end_hour, int) or not (0 <= mild_penalty_end_hour <= 23):
                raise ValueError(
                    f"Invalid 'mild_penalty_end_hour' value: {mild_penalty_end_hour!r}. Must be an integer between 0 and 23."
                )

            # Load window patterns with their score values
            window_patterns = []
            for pattern in config_data.get("window_patterns", []):
                window_patterns.append(
                    {
                        "regex": pattern.get("regex", ""),
                        "score": pattern.get("score", 0),
                        "description": pattern.get("description", ""),
                    }
                )

            # Only update instance attributes after successful parsing
            self.default_score = default_score
            self.apply_default_score_mode = apply_default_score_mode
            self.always_on_top = always_on_top
            self.hide_on_mouse_proximity = hide_on_mouse_proximity
            self.proximity_distance = proximity_distance
            self.mild_penalty_mode = mild_penalty_mode
            self.mild_penalty_start_hour = mild_penalty_start_hour
            self.mild_penalty_end_hour = mild_penalty_end_hour
            self.window_patterns = window_patterns

            # Update last modified timestamp after successful load
            self._last_modified = self.config_path.stat().st_mtime

        except FileNotFoundError:
            if exit_on_error:
                print(f"Error: Configuration file '{self.config_path}' not found.")
                sys.exit(1)
            else:
                raise
        except Exception as e:
            if exit_on_error:
                print(f"Error: Failed to load configuration: {e}")
                sys.exit(1)
            else:
                raise

    def is_modified(self):
        """Check if configuration file has been modified.

        Returns:
            bool: True if file has been modified since last load, False otherwise
        """
        try:
            current_mtime = self.config_path.stat().st_mtime
            return current_mtime != self._last_modified
        except Exception:
            return False

    def reload_if_modified(self):
        """Reload configuration if the file has been modified.

        Returns:
            bool: True if configuration was reloaded, False otherwise
        """
        if self.is_modified():
            try:
                self.load_config(exit_on_error=False)
                print(f"Configuration reloaded from '{self.config_path}'")
                return True
            except Exception as e:
                print(f"Warning: Failed to reload configuration: {e}")
                return False
        return False

    def get_window_patterns(self):
        """Get list of window patterns.

        Returns:
            list: List of pattern dictionaries with regex, score, and description
        """
        return self.window_patterns

    def get_default_score(self):
        """Get default score for non-matching windows.

        Returns:
            int: Default score value
        """
        return self.default_score

    def get_apply_default_score_mode(self):
        """Get apply_default_score_mode setting.

        Returns:
            bool: True if default score should be applied when no pattern matches, False otherwise
        """
        return self.apply_default_score_mode

    def get_always_on_top(self):
        """Get always_on_top setting.

        Returns:
            bool: True if window should stay on top, False otherwise
        """
        return self.always_on_top

    def get_hide_on_mouse_proximity(self):
        """Get hide_on_mouse_proximity setting.

        Returns:
            bool: True if window should hide when mouse is near, False otherwise
        """
        return self.hide_on_mouse_proximity

    def get_proximity_distance(self):
        """Get proximity_distance setting.

        Returns:
            int: Distance in pixels to trigger proximity behavior
        """
        return self.proximity_distance

    def get_mild_penalty_mode(self):
        """Get mild_penalty_mode setting.

        Returns:
            bool: True if mild penalty mode is enabled, False otherwise
        """
        return self.mild_penalty_mode

    def get_mild_penalty_start_hour(self):
        """Get mild_penalty_start_hour setting.

        Returns:
            int: Start hour for mild penalty mode (0-23)
        """
        return self.mild_penalty_start_hour

    def get_mild_penalty_end_hour(self):
        """Get mild_penalty_end_hour setting.

        Returns:
            int: End hour for mild penalty mode (0-23)
        """
        return self.mild_penalty_end_hour

{% endraw %}
```

## 最近の変更（過去7日間）
### コミット履歴:
b1fc7df Merge pull request #22 from cat2151/copilot/add-mode-for-score-adjustment
bf5b754 Improve test_apply_default_score_mode_update_config to verify score_changed and use consistent window title
34676a8 Add apply_default_score_mode to enable/disable default score application
4185798 Initial plan
a90c8cb Add issue note for #21 [auto]
615a905 Merge pull request #20 from cat2151/copilot/toggle-score-penalty-mode
21a57fc Add boolean type validation for mild_penalty_mode config
12c6884 Add mild penalty mode feature with TOML configuration
1575bda Initial plan
a05340f Enhance issue 15 notes with implementation details

### 変更されたファイル:
README.ja.md
README.md
config.toml.example
issue-notes/15.md
issue-notes/21.md
src/config.py
src/gui.py
src/main.py
src/score_tracker.py
tests/test_config.py
tests/test_gui.py
tests/test_score_tracker.py


---
Generated at: 2025-12-29 07:05:31 JST
