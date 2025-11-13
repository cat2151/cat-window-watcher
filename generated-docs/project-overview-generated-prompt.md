Last updated: 2025-11-12


# プロジェクト概要生成プロンプト（来訪者向け）

## 生成するもの：
- projectを3行で要約する
- プロジェクトで使用されている技術スタックをカテゴリ別に整理して説明する
- プロジェクト全体のファイル階層ツリー（ディレクトリ構造を図解）
- プロジェクト全体のファイルそれぞれの説明
- プロジェクト全体の関数それぞれの説明
- プロジェクト全体の関数の呼び出し階層ツリー

## 生成しないもの：
- Issues情報（開発者向け情報のため）
- 次の一手候補（開発者向け情報のため）
- ハルシネーションしそうなもの（例、存在しない機能や計画を勝手に妄想する等）

## 出力フォーマット：
以下のMarkdown形式で出力してください：

```markdown
# Project Overview

## プロジェクト概要
[以下の形式で3行でプロジェクトを要約]
- [1行目の説明]
- [2行目の説明]
- [3行目の説明]

## 技術スタック
[使用している技術をカテゴリ別に整理して説明]
- フロントエンド: [フロントエンド技術とその説明]
- 音楽・オーディオ: [音楽・オーディオ関連技術とその説明]
- 開発ツール: [開発支援ツールとその説明]
- テスト: [テスト関連技術とその説明]
- ビルドツール: [ビルド・パース関連技術とその説明]
- 言語機能: [言語仕様・機能とその説明]
- 自動化・CI/CD: [自動化・継続的統合関連技術とその説明]
- 開発標準: [コード品質・統一ルール関連技術とその説明]

## ファイル階層ツリー
```
[プロジェクトのディレクトリ構造をツリー形式で表現]
```

## ファイル詳細説明
[各ファイルの役割と機能を詳細に説明]

## 関数詳細説明
[各関数の役割、引数、戻り値、機能を詳細に説明]

## 関数呼び出し階層ツリー
```
[関数間の呼び出し関係をツリー形式で表現]
```
```


以下のプロジェクト情報を参考にして要約を生成してください：

## プロジェクト情報
名前: 
説明: # cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that tracks your active window and adjusts a score based on what you're doing.

## WIP

開発中です。ここに書いてあるものは、「それを目指している」というレベルです。実装されていない可能性があります。

## ⚠️ Provisional Implementation Notice

This is a **provisional implementation for testing and verification purposes**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps in this phase)
- Straightforward logic: checks active window title every 1 second
- Minimal complexity to facilitate rapid development and testing

Future versions may include optimizations and integrations, but this version prioritizes simplicity and ease of understanding.

## Concept

The application monitors which window is currently active and adjusts a score based on configurable patterns:
- Working on GitHub? Score increases! 🎉
- Browsing social media? Score decreases... 😿

The cat is watching you!

## Features

- **Simple Score Display**: Shows your current score in a clean tkinter GUI
- **Regex-based Window Matching**: Configure window title patterns using regular expressions
- **Configurable Score Values**: Set custom score increase/decrease amounts for each pattern
- **Cross-platform Support**: Works on Linux, macOS, and Windows
- **Lightweight**: Checks window title once per second, minimal resource usage

## What It Looks Like

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

The GUI features a dark theme with a large score display and status showing your current activity.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cat2151/cat-window-watcher.git
cd cat-window-watcher
```

2. Ensure you have Python 3.12+ installed:
```bash
python --version
```

3. Install dependencies (if needed):
   - Linux: `xdotool` or `xprop` (usually pre-installed)
   - macOS: Built-in AppleScript support
   - Windows: Works with built-in APIs (optional: `pywin32` for better support)

## Configuration

1. Copy the example configuration:
```bash
cp config.toml.example config.toml
```

2. Edit `config.toml` to customize window patterns and scores:

```toml
[[window_patterns]]
regex = "github"           # Regex pattern to match window title
score = 10                 # Score change when this window is active
description = "GitHub"     # Display description

[[window_patterns]]
regex = "twitter|x\\.com"
score = -5
description = "Twitter/X"
```

### Configuration Options

- **regex**: Regular expression pattern to match against window titles (case-insensitive)
- **score**: Integer value to add to score when pattern matches (can be negative)
- **description**: Human-readable description shown in the status area

## Usage

Run the application:
```bash
# Method 1: Direct script execution
python src/main.py

# Method 2: Run as module
python -m src

# Method 3: With custom config file
python src/main.py --config my_config.toml
python src/main.py -c my_config.toml
```

The GUI will display:
- Current score in large text
- Status showing the current matched pattern or window title
- Updates every second automatically

## Examples

### Example 1: Productivity Tracking
```toml
[[window_patterns]]
regex = "github|gitlab"
score = 10
description = "Coding"

[[window_patterns]]
regex = "twitter|facebook|instagram"
score = -5
description = "Social Media"
```

### Example 2: Study Time
```toml
[[window_patterns]]
regex = "pdf|documentation|docs"
score = 8
description = "Reading"

[[window_patterns]]
regex = "youtube|netflix"
score = -10
description = "Entertainment"
```

## Development

### Running Tests
```bash
python -m unittest discover tests/ -v
```

### Code Formatting
Format code before committing:
```bash
ruff format src/ tests/
ruff check --fix src/ tests/
```

### Linting
Verify code quality:
```bash
ruff format --check src/ tests/
ruff check src/ tests/
```

## Architecture

The application consists of several modules:

- **config.py**: Loads and manages TOML configuration
- **window_monitor.py**: Cross-platform window title detection
- **score_tracker.py**: Matches window titles against patterns and tracks score
- **gui.py**: tkinter-based score display interface
- **main.py**: Application entry point and orchestration

## Platform-Specific Notes

### Linux
Requires `xdotool` or `xprop`:
```bash
sudo apt-get install xdotool  # Debian/Ubuntu
```

### macOS
Uses built-in AppleScript. No additional dependencies required.

### Windows
Works with built-in Windows APIs. For better compatibility, install:
```bash
pip install pywin32
```

## License

See LICENSE file for details.

*Big Brother is watching you. But this time, it's a cat. 🐱*


依存関係:
{}

## ファイル階層ツリー
📄 .editorconfig
📄 .gitignore
📄 .pre-commit-config.yaml
📁 .vscode/
  📊 settings.json
📄 LICENSE
📖 README.md
📖 USAGE.md
📄 _config.yml
📄 config.toml.example
📁 examples/
  📄 example.txt
📁 generated-docs/
📄 pytest.ini
📄 ruff.toml
📁 src/
  📄 __init__.py
  📄 __main__.py
  📄 config.py
  📄 gui.py
  📄 main.py
  📄 score_tracker.py
  📄 window_monitor.py
📁 tests/
  📄 test_config.py
  📄 test_dummy.py
  📄 test_score_tracker.py
  📄 test_window_monitor.py

## ファイル詳細分析


## 関数呼び出し階層
関数呼び出し階層を分析できませんでした

## プロジェクト構造（ファイル一覧）
.vscode/settings.json
README.md
USAGE.md

上記の情報を基に、プロンプトで指定された形式でプロジェクト概要を生成してください。
特に以下の点を重視してください：
- 技術スタックは各カテゴリごとに整理して説明
- ファイル階層ツリーは提供された構造をそのまま使用
- ファイルの説明は各ファイルの実際の内容と機能に基づく
- 関数の説明は実際に検出された関数の役割に基づく
- 関数呼び出し階層は実際の呼び出し関係に基づく


---
Generated at: 2025-11-12 07:05:54 JST
