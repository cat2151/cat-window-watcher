Last updated: 2026-01-01

# Development Status

## 現在のIssues
- [Issue #42](../issue-notes/42.md) と [Issue #39](../issue-notes/39.md) は、アプリケーションウィンドウの初期表示位置をTOML設定ファイル（`window_x`, `window_y`）でカスタマイズする機能の追加を目指しています。
- [Issue #26](../issue-notes/26.md) は、開発者が自身でアプリケーションを日常的に使用（ドッグフーディング）し、実際の使用感に基づいた改善点を見つけることを目的としています。
- [Issue #9](../issue-notes/9.md) は、ウィンドウタイトルが設定されたパターンにマッチしない場合に、デフォルトのスコアを定義することで設定ミスを早期に検知しやすくする改善を提案しています。

## 次の一手候補
1. アプリケーションウィンドウの初期表示位置をTOMLで設定できるようにする [Issue #42](../issue-notes/42.md)
   - 最初の小さな一歩: `src/config.py` に `window_x` と `window_y` の読み込みロジックを追加し、デフォルト値をNoneに設定する。
   - Agent実行プロンプト:
     ```
     対象ファイル: src/config.py, config.toml.example

     実行内容: `src/config.py` に、`config.toml.example` の設定を参考に、`window_x` と `window_y` (int型、デフォルトはNone) をTOMLから読み込む機能を追加してください。`config.toml.example` にもこれらの設定項目を追加してください。

     確認事項: 既存の`load_config`関数との整合性、型変換時のエラーハンドリング（Noneまたはint型以外の値の場合）、および他の設定項目との競合がないことを確認してください。`window_x`と`window_y`が負の値を取りうることも考慮してください。

     期待する出力: `src/config.py` と `config.toml.example` の変更内容を記載したコードブロック。
     ```

2. マッチしない場合のデフォルトスコアをTOMLで設定できるようにする [Issue #9](../issue-notes/9.md)
   - 最初の小さな一歩: `src/config.py` に `default_unmatched_score` の読み込みロジックを追加し、`config.toml.example` にも設定項目を追加する。
   - Agent実行プロンプト:
     ```
     対象ファイル: src/config.py, src/score_tracker.py, config.toml.example

     実行内容: `src/config.py` に `default_unmatched_score` (int型、デフォルトは例えば-1) をTOMLから読み込む機能を追加し、`config.toml.example` にもこの設定項目を追加してください。また、`src/score_tracker.py` でウィンドウタイトルがどのパターンにもマッチしなかった場合に、この `default_unmatched_score` を使用するように修正してください。

     確認事項: 既存のスコア計算ロジックとの整合性、負のスコアが適切に扱われるか、および設定値が有効な数値であることを確認してください。

     期待する出力: `src/config.py`, `src/score_tracker.py`, `config.toml.example` の変更内容を記載したコードブロック。
     ```

3. ドッグフーディング開始の準備とフィードバック収集 [Issue #26](../issue-notes/26.md)
   - 最初の小さな一歩: 開発者がアプリケーションを日常的に利用し始めるための最小限のガイダンスを`README.md`に追記する。
   - Agent実行プロンプト:
     ```
     対象ファイル: README.md, README.ja.md

     実行内容: `README.md` と `README.ja.md` に「Dogfooding / ドッグフーディング」セクションを追加し、開発者がアプリケーションをどのように日常的に使用し、フィードバックをどのように収集するか（例: 新しいIssueを立てる、既存のIssueにコメントする）についての簡単なガイドラインを記述してください。

     確認事項: 既存のREADME構造との整合性、簡潔で分かりやすい説明になっているか、および具体的なフィードバック経路が示されていることを確認してください。

     期待する出力: `README.md` と `README.ja.md` の変更内容を記載したコードブロック。
     ```

---
Generated at: 2026-01-01 07:05:52 JST
