# ゲームプレイ検知機能の使い方

## 概要

この機能は、ストリートファイター6などのゲームをプレイ中に、cat-window-watcherの更新頻度を自動的に下げることができます。通常は1秒ごとにチェックしますが、ゲームプレイ中は1分（60秒）ごとのチェックに切り替わり、リソース消費を抑えます。

## 設定方法

### 1. config.tomlに追加

`config.toml`ファイルに以下のセクションを追加してください：

```toml
[game_playing_detection]
enabled = true
process_names = ["StreetFighter6.exe", "SF6.exe"]
check_interval_seconds = 60
```

### 2. パラメータの説明

- **enabled**: `true`でゲーム検知を有効化、`false`で無効化
- **process_names**: 検知したいゲームのプロセス名のリスト
  - Windows: 実行ファイル名（例: `StreetFighter6.exe`）
  - macOS: アプリケーション名（例: `Street Fighter 6`）
  - Linux: プロセス名（例: `sf6`, `streetfighter6`）
- **check_interval_seconds**: ゲーム検知時のチェック間隔（秒）
  - デフォルト: 60秒
  - 推奨: 30〜120秒

## プロセス名の確認方法

### Windows
```powershell
# タスクマネージャーで確認
# または PowerShellで:
Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object ProcessName, MainWindowTitle
```

### macOS
```bash
# アクティビティモニタで確認
# またはターミナルで:
osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true'
```

### Linux
```bash
# System Monitorで確認
# またはターミナルで:
ps aux | grep -i streetfighter
# または xdotool で:
xdotool getactivewindow getwindowpid | xargs ps -p -o comm=
```

## 動作確認

アプリを起動して、ゲームを開始すると以下のメッセージが表示されます：

```
Game detected (StreetFighter6.exe), switching to 60 second check interval
```

ゲームを終了すると：

```
Game ended, switching back to 1 second check interval
```

## 設定例

### ストリートファイター6
```toml
[game_playing_detection]
enabled = true
process_names = ["StreetFighter6.exe", "SF6.exe"]
check_interval_seconds = 60
```

### 複数のゲームを検知
```toml
[game_playing_detection]
enabled = true
process_names = [
    "StreetFighter6.exe",
    "TEKKEN8.exe",
    "GGST-Win64-Shipping.exe"
]
check_interval_seconds = 60
```

### より短い間隔でチェック
```toml
[game_playing_detection]
enabled = true
process_names = ["StreetFighter6.exe"]
check_interval_seconds = 30  # 30秒ごとにチェック
```

## トラブルシューティング

### ゲームが検知されない

1. プロセス名が正しいか確認してください
   - 大文字小文字を区別します
   - 拡張子（.exe）も含めてください（Windows）

2. 管理者権限で実行してみてください
   - 一部のゲームは管理者権限が必要な場合があります

3. デバッグ出力を確認してください
   - ターミナルでアプリを起動すると、検知状態が表示されます

### チェック間隔が変わらない

1. `enabled = true`になっているか確認してください
2. 設定ファイルの構文が正しいか確認してください
3. アプリを再起動してください

## 参考

この機能は[fighting-game-button-challenge](https://github.com/cat2151/fighting-game-button-challenge)リポジトリの実装を参考にしています。
