# 設定例

このディレクトリには、cat-window-watcher の設定例ファイルが含まれています。各例は、異なる使用例と設定パターンを示しています。

## 利用可能な例

### 例1: 生産性の追跡
- **英語版**: [example1_productivity.toml](example1_productivity.toml)
- **日本語版**: [example1_productivity.ja.toml](example1_productivity.ja.toml)

仕事関連のウィンドウ（GitHub、GitLab）とソーシャルメディアを監視して生産性を追跡します。

### 例2: 勉強時間
- **英語版**: [example2_study_time.toml](example2_study_time.toml)
- **日本語版**: [example2_study_time.ja.toml](example2_study_time.ja.toml)

勉強や読書の時間（PDF、ドキュメント）とエンターテイメント（YouTube、Netflix）を追跡します。

### 例3: 最前面モードでマウス接近時に自動で最背面に移動
- **英語版**: [example3_always_on_top.toml](example3_always_on_top.toml)
- **日本語版**: [example3_always_on_top.ja.toml](example3_always_on_top.ja.toml)

最前面表示機能と、マウスがウィンドウに近づいたときの自動非表示機能を示します。

## 例の使用方法

例の設定を使用するには：

```bash
# 例を config.toml にコピー
cp examples/example1_productivity.ja.toml config.toml

# または特定の例を直接実行
python src/main.py --config examples/example1_productivity.ja.toml
```

## 独自の設定を作成する

これらの例を独自の設定の出発点として使用できます。異なる例の機能を組み合わせたり、ニーズに基づいてまったく新しいパターンを作成したりできます。

設定オプションの詳細については、メインの [README.md](../README.md) または [README.ja.md](../README.ja.md) を参照してください。
