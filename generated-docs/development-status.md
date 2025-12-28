Last updated: 2025-12-29

# Development Status

## 現在のIssues
- [Issue #23](../issue-notes/23.md)と[Issue #13](../issue-notes/13.md)は、スコアの増減状態に応じて表示色を（特に減少時に赤く）変更する設定をTOMLで可能にする機能追加を検討中です。
- [Issue #16](../issue-notes/16.md)は、ポモドーロ・テクニックのように30分ごとにスコアをリセットする機能をTOMLでオンオフ可能にすることを提案しています。
- [Issue #14](../issue-notes/14.md)は、ユーザーのフロー状態没入を助けるため、スコアアップ後10秒でウィンドウを徐々に透明にするモードをTOMLで追加することを提案しています。

## 次の一手候補
1. [Issue #23](../issue-notes/23.md): スコア増減時の表示色をTOMLで設定可能にする（[Issue #13](../issue-notes/13.md)を含む）
   - 最初の小さな一歩: `src/config.py`に`score_up_color`と`score_down_color`の設定を読み込むロジックを実装し、これらの設定が有効なHEXカラーコードであることを検証する。
   - Agent実行プロンプト:
     ```
     対象ファイル: `src/config.py`, `config.toml.example`

     実行内容: `src/config.py`に`score_up_color` (デフォルト: `#ffffff`) と`score_down_color` (デフォルト: `#ff0000`) の新しい設定項目を追加し、`config.toml.example`にもこれらを反映させてください。`load_config`メソッド内で、これらの値が有効な16進数カラーコード（例: `#RRGGBB`）であることを検証するロジックを実装してください。無効な場合は`ValueError`を発生させます。

     確認事項: 既存のTOML設定の読み込みロジック（特に`default_score`やその他の色設定以外の項目）との整合性、およびエラーハンドリングが適切に機能することを確認してください。カラーコードの検証は正規表現（例: `#([0-9a-fA-F]{3}){1,2}`）を使用し、`ValueError`のメッセージは具体的かつ明確に記述してください。

     期待する出力: `src/config.py`が更新され、新しいカラー設定の読み込みと検証ロジックが追加されたPythonコード。`config.toml.example`が更新され、新しい設定項目が追加されたTOML設定ファイル。
     ```

2. [Issue #16](../issue-notes/16.md): 30分ごとのスコアリセット機能をTOMLでon/off可能にする
   - 最初の小さな一歩: `src/config.py`に`reset_score_every_30_minutes`のようなブール値設定を追加し、`config.toml.example`にその設定例を記述する。
   - Agent実行プロンプト:
     ```
     対象ファイル: `src/config.py`, `config.toml.example`

     実行内容: `src/config.py`の`Config`クラスに、30分ごとのスコアリセットを有効にするためのブール値設定（例: `reset_score_every_30_minutes`, デフォルトは`false`）を追加し、`load_config`メソッドでTOMLから読み込むように変更してください。`load_config`メソッド内で、この設定値がブール型であることを検証し、異なる場合は`ValueError`を発生させます。また、`config.toml.example`にこの新しい設定項目を追加してください。

     確認事項: 新しい設定が既存の設定ロジックと衝突しないか、適切なデフォルト値と型検証が設定されているかを確認してください。`mild_penalty_mode`の検証ロジックを参考に実装してください。

     期待する出力: `src/config.py`が更新され、新しいスコアリセット設定の読み込みロジックが追加されたPythonコード。`config.toml.example`が更新され、新しい設定項目が追加されたTOML設定ファイル。
     ```

3. [Issue #14](../issue-notes/14.md): スコアアップ後ウィンドウを徐々に透明にするモードをTOMLでon/off可能にする
   - 最初の小さな一歩: `src/config.py`に`fade_window_on_flow_mode_enabled` (bool), `flow_mode_delay_seconds` (int), `flow_mode_fade_rate_percent_per_second` (int) の設定を追加し、`config.toml.example`にその設定例を記述する。
   - Agent実行プロンプト:
     ```
     対象ファイル: `src/config.py`, `config.toml.example`

     実行内容: `src/config.py`の`Config`クラスに、フロー状態没入をサポートするためのウィンドウ透明化モードに関する設定項目（例: `fade_window_on_flow_mode_enabled` (bool, デフォルト: `false`), `flow_mode_delay_seconds` (int, デフォルト: `10`), `flow_mode_fade_rate_percent_per_second` (int, デフォルト: `1`)）を追加し、`load_config`メソッドでTOMLから読み込むように変更してください。各設定値について、適切な型検証と範囲チェック（例: `flow_mode_delay_seconds >= 0`, `0 < flow_mode_fade_rate_percent_per_second <= 100`）を実装し、無効な場合は`ValueError`を発生させます。`config.toml.example`にもこれらの新しい設定項目を追加してください。

     確認事項: 新しい設定が既存の設定ロジックと衝突しないか、適切なデフォルト値と厳密な型・範囲検証が設定されているかを確認してください。特に数値設定の境界値（0や100）での挙動を考慮した検証ロジックにしてください。

     期待する出力: `src/config.py`が更新され、新しいウィンドウ透明化モード設定の読み込みロジックが追加されたPythonコード。`config.toml.example`が更新され、新しい設定項目が追加されたTOML設定ファイル。

---
Generated at: 2025-12-29 07:05:50 JST
