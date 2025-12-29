Last updated: 2025-12-30

# Development Status

## 現在のIssues
- 現在のオープンIssueである [Issue #26](../issue-notes/26.md) は、`cat-window-watcher`を開発者自身が日常的に使用し、潜在的な改善点や不便な点を特定する「ドッグフーディング」プロセスを開始することを目指しています。
- [Issue #6](../issue-notes/6.md) は、GitHubのプルリクエストやコード表示ページが、ウィンドウタイトルに「GitHub」を含まないためにアプリケーションによって正しく「GitHubサイト」と認識されない問題を提起しており、ウィンドウ認識ロジックの改善が必要です。
- これらの課題を通じて、アプリケーションの実際の使用感を高め、特定のウェブサイトに対する認識精度を向上させることが現在の主要な開発目標となっています。

## 次の一手候補
1. [Issue #26](../issue-notes/26.md): ドッグフーディングのための観察・記録ガイドラインを作成する
   - 最初の小さな一歩: `cat-window-watcher`を日常的に使用する際に、どのような点に注目し、何を記録すべきかについての具体的なガイドラインを作成する。これにより、効果的なドッグフーディングの第一歩を踏み出す。
   - Agent実行プロンプト:
     ```
     対象ファイル: なし (新規作成のガイドライン)

     実行内容: [Issue #26](../issue-notes/26.md)「ドッグフーディングする」の実行をサポートするため、`cat-window-watcher`を日常的に使用する際に「何に着目し、何を記録すべきか」についてのガイドラインをmarkdown形式で作成してください。以下の観点を含めてください：
     1. アプリケーションの起動と停止の際の感覚
     2. ウィンドウ認識の誤りや認識漏れ（特に[Issue #6](../issue-notes/6.md)のような具体的なケース）
     3. スコアの変動と視覚的フィードバックの適切さ
     4. 新機能（最前面表示、不透明度遷移）のトリガーと効果
     5. GUI操作の直感性や設定変更の容易さ

     確認事項: 具体的なコード変更を伴わない、あくまでドッグフーディングのための「観点と記録内容」に焦点を当てること。ハルシネーションを避け、既存の機能やIssueに基づいた内容にすること。

     期待する出力: ドッグフーディング時に活用できる「観察・記録ガイドライン」をmarkdown形式で出力してください。
     ```

2. [Issue #6](../issue-notes/6.md): GitHubのプルリクエスト/コードページ認識問題を調査し修正案を提案する
   - 最初の小さな一歩: 実際のGitHubのプルリクエストやコード表示ページで取得されるウィンドウタイトルとクラス名の具体的なパターンを特定し、`src/window_monitor.py`のロジックと`config.toml.example`の設定がどのように異なるかを確認する。
   - Agent実行プロンプト:
     ```
     対象ファイル: `src/window_monitor.py`, `config.toml.example`

     実行内容: [Issue #6](../issue-notes/6.md)で報告されている、GitHubのプルリクエストやコードページが正しく認識されない問題について、原因特定のための分析を行ってください。具体的には：
     1. `src/window_monitor.py`内の`get_active_window_info`関数が、これらのページでどのようなウィンドウタイトルとウィンドウクラス名を返すかを推測してください。
     2. `config.toml.example`内の`[sites.github]`セクションの`title_keywords`と`class_keywords`が、現在のGitHubのPR/Codeページのウィンドウ情報とどのように合致しない可能性があるかを分析してください。
     3. 認識を改善するために、`config.toml.example`の`[sites.github]`セクションにどのような`title_keywords`または`class_keywords`を追加・修正すべきか、具体的な提案を記述してください。

     確認事項: GitHubのページの実際のウィンドウタイトルは環境によって異なる可能性があるため、一般的なパターンを想定して分析すること。ハルシネーションを避け、既存のコードと設定ファイルの内容に基づいて分析すること。

     期待する出力: 上記の分析結果と、`config.toml.example`の改善提案を含むmarkdown形式の分析レポート。
     ```

3. 新機能（`always_on_top_while_score_decreasing`）をGUIに統合する
   - 最初の小さな一歩: `src/gui.py`内の既存の設定項目がどのようにGUIに反映されているかを調査し、`always_on_top_while_score_decreasing`設定をGUIに追加するためのUI要素（チェックボックスなど）の配置と、そのUI要素と設定値の連動方法を検討する。
   - Agent実行プロンプト:
     ```
     対象ファイル: `src/gui.py`, `src/config.py`, `config.toml.example`

     実行内容: `src/gui.py`と`src/config.py`、および`config.toml.example`を分析し、最近追加された`always_on_top_while_score_decreasing`設定をGUIからON/OFFできるようにするための改修案を提案してください。具体的には：
     1. `src/gui.py`のどの部分に新しいUI要素（例: チェックボックス）を追加すべきか。
     2. そのUI要素と`src/config.py`の対応する設定値（`always_on_top_while_score_decreasing`）をどのように同期させるか（アプリケーション起動時の読み込みと、GUI操作による保存）。
     3. 設定が永続化されるように`src/config.py`およびGUI側の保存ロジックにどのような変更が必要か検討してください。

     確認事項: 既存のGUIのレイアウトや設定管理ロジックを尊重し、整合性を保つこと。PyQt/PySide2 (または使用されているGUIライブラリ) の一般的な実装パターンに従うこと。

     期待する出力: `always_on_top_while_score_decreasing`設定をGUIに統合するための具体的なコード変更箇所の説明と、擬似コードを含むmarkdown形式の提案。
     ```

---
Generated at: 2025-12-30 07:06:04 JST
