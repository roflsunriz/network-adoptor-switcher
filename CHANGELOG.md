# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-02-14

### Fixed
- **PowerShellウィンドウの非表示**: EXE実行時にPowerShellのコンソールウィンドウが一瞬表示される問題を修正
  - `subprocess.run()` に `CREATE_NO_WINDOW` フラグを追加
  - これにより、ネットワークアダプター操作時にコンソールが表示されなくなりました

### Technical Details
- `src/network_manager.py` に `CREATE_NO_WINDOW` 定数を追加（Windows専用）
- すべての `subprocess.run()` 呼び出しに `creationflags=CREATE_NO_WINDOW` を追加
- 3箇所の修正: `get_adapters()`, `enable_adapter()`, `disable_adapter()`

## [1.0.0] - 2026-02-14

### Added
- 初回リリース
- イーサネットとWi-Fiアダプターの自動検出機能
- ワンクリックでのアダプター排他的切り替え
- リアルタイムアダプター状態表示
- 管理者権限チェック
- tkinter GUIインターフェース
- PyInstallerによるEXEビルド対応
- UTF-8エンコーディング対応（Windows PowerShell）
- 包括的な単体テスト（33テスト）
- 型安全性（mypy strict mode）
- コード品質管理（ruff, black）

### Features
- **自動アダプター検出**: システム上のイーサネットとWi-Fiアダプターを自動で識別
- **排他的切り替え**: 一方を無効化して他方を自動的に有効化
- **状態表示**: 各アダプターの有効/無効状態をリアルタイム表示
- **エラーハンドリング**: 詳細なエラーメッセージとログ記録
- **スタンドアロンEXE**: Python環境不要の単一実行ファイル
