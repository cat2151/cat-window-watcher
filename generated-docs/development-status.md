Last updated: 2026-02-06

# Development Status

## 現在のIssues
- [Issue #26](../issue-notes/26.md) はプロジェクトの「ドッグフーディング」を目的とし、自身のツールを使用することによる改善を目指しています。
- [Issue #6](../issue-notes/6.md) では、GitHubサイトの特定のページ（Pull requests, Codeなど）がウィンドウタイトルに含まれる単語だけではGitHubサイトとして正しく認識されない問題が指摘されています。
- 最近の更新では、[Issue #80](../issue-notes/80.md) に関連してStreet Fighter 6などのゲーム検出機能が追加され、その詳細化やドキュメント化が進められています。

## 次の一手候補
1. GitHubサイトのウィンドウタイトル認識問題 [Issue #6](../issue-notes/6.md) を修正する
   - 最初の小さな一歩: `src/window_monitor.py` がどのようにアクティブウィンドウのタイトルを取得し、カテゴリを判断しているか、および `config.toml.example` でGitHubカテゴリがどのように定義されているかを調査する。特に、Pull requestsやCodeページのタイトルが、現在の設定でどのようにマッチしているか（またはしていないか）を確認する。
   - Agent実行プロンプト:
     ```
     対象ファイル: `src/window_monitor.py`, `src/config_loader.py`, `src/config.py`, `config.toml.example`

     実行内容:
     1. `src/window_monitor.py` と `src/config_loader.py` におけるウィンドウタイトル取得・処理ロジックを分析する。
     2. `config.toml.example` のGitHubカテゴリ定義を確認し、[Issue #6](../issue-notes/6.md) で言及されている「Pull requests」や「Code」ページを閲覧した際の典型的なウィンドウタイトル例を考慮に入れる。
     3. `src/config.py` 内でカテゴリマッチングに使用される正規表現や文字列比較のメカニズムを特定する。
     4. 現状の設定で、これらのGitHubページのタイトルがなぜ認識されないのか、考えられる原因を特定する。

     確認事項:
     - ウィンドウタイトルの取得方法がOSによって異なる可能性がないか確認する。
     - 既存のカテゴリマッチングロジックが他のサイトに影響を与えないことを確認する。
     - `config.toml.example` の変更が`config_validator.py`による検証をパスするか確認する。

     期待する出力:
     - [Issue #6](../issue-notes/6.md) の原因分析結果をmarkdown形式で出力する。
     - 提案される修正案（例: `config.toml.example`の正規表現修正案、`src/window_monitor.py`での追加ロジック、または`src/config.py`のカテゴリマッチング改善案）を提示する。
     - これらの修正によって影響を受ける可能性のあるファイルとその理由を記述する。
     ```

2. ドッグフーディングの一環として、現在の開発フローに基づいたカテゴリ定義のレビューと改善 [Issue #26](../issue-notes/26.md)
   - 最初の小さな一歩: 自身の開発作業中に使用するアプリケーション（IDE, ブラウザ, ターミナルなど）と、それぞれのウィンドウタイトルから識別可能なキーワードをリストアップする。現在の `config.toml.example` と比較し、不足しているカテゴリや最適化可能な定義を特定する。
   - Agent実行プロンプト:
     ```
     対象ファイル: `config.toml.example`, `src/config.py`

     実行内容:
     1. 現在の `config.toml.example` に定義されているカテゴリと、そのマッチングルールを詳細に分析する。
     2. 開発者が日常的に利用する主要なツール（例: VS Code, Chrome, Terminal, GitKrakenなど）を想定し、これらのツールで作業する際の典型的なウィンドウタイトルパターンを洗い出す。
     3. 現行の `config.toml.example` の定義が、洗い出したウィンドウタイトルパターンを適切にカバーしているか評価する。特に、`[category.development]` や `[category.communication]` など、開発に関連するカテゴリ定義に焦点を当てる。
     4. 不足しているカテゴリや、より精密なマッチングを可能にするための新しい `category` や `pattern` の追加・修正案を検討する。

     確認事項:
     - 提案する新しいカテゴリ定義が既存のカテゴリと衝突しないか確認する。
     - 汎用性が高く、他のユーザーにも利用可能なカテゴリ定義になっているか考慮する。
     - `src/config_validator.py` による設定ファイルの検証ロジックと整合性が取れているか確認する。

     期待する出力:
     - 自身の開発フローを効率的にトラッキングするための `config.toml.example` の改善提案をmarkdown形式で出力する。
     - 具体的には、新しいカテゴリ（例: `[category.code_review]`, `[category.documentation]`）や、既存カテゴリの `patterns` を追加・修正する具体的な設定例を提示する。
     - これらの変更が `src/config.py` のどの部分に影響を与える可能性があるかを記述する。
     ```

3. ゲーム検出機能の汎用化と設定ファイル（`config.toml.example`）の拡充 [Issue #80](../issue-notes/80.md) 関連
   - 最初の小さな一歩: `config.toml.example` の `[game_detection]` セクションと、`docs/game-detection-guide.md` をレビューし、現在Street Fighter 6に特化している部分を特定する。
   - Agent実行プロンプト:
     ```
     対象ファイル: `config.toml.example`, `docs/game-detection-guide.md`, `src/config_loader.py`, `src/window_monitor.py`

     実行内容:
     1. `config.toml.example` に存在するゲーム検出関連の設定（`[game_detection]`セクション）を分析し、現状でStreet Fighter 6に特化している箇所を特定する。
     2. `docs/game-detection-guide.md` をレビューし、ゲーム検出機能のセットアップ手順と、新しいゲームを追加するためのガイダンスが明確かつ汎用的であるか評価する。
     3. 他の一般的なゲーム（例: Apex Legends, Valorant, Minecraftなど）を検出するための `config.toml.example` の設定例を複数考案し、これらがユーザーにとって理解しやすい形式であることを確認する。
     4. `src/config_loader.py` および `src/window_monitor.py` が、汎用的なゲーム検出設定に対応できる設計になっているかを確認し、必要に応じてリファクタリングの可能性を検討する。

     確認事項:
     - 新しいゲーム検出の例が既存の `config.toml.example` の構造と整合性が取れているか確認する。
     - `docs/game-detection-guide.md` の更新が、ユーザーが容易に新しいゲームを追加できるよう導く内容になっているか確認する。
     - `src/config_validator.py` によってゲーム検出の設定が正しく検証されるか確認する。

     期待する出力:
     - 複数のゲームに対応するための `config.toml.example` の更新案をmarkdown形式で出力する。具体的には、`[game_detection]` セクションに複数のゲームエントリを追加する形式を提案する。
     - `docs/game-detection-guide.md` の更新内容として、新しいゲームを追加する具体的な手順や、推奨される設定方法を記述する。
     - `src/config_loader.py` や `src/window_monitor.py` 側で汎用化のために必要な変更点や考慮事項を記述する。
     ```

---
Generated at: 2026-02-06 07:08:32 JST
