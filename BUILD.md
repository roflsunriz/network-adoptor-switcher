# ビルドガイド

このドキュメントでは、ネットワークアダプター切り替えツールのEXEファイルをビルドする方法を説明します。

## 前提条件

- Python 3.10以降がインストールされていること
- 仮想環境が作成されていること（`venv`フォルダ）
- PyInstallerがインストールされていること（自動でインストールされます）

## 自動ビルド（推奨）

プロジェクトルートで以下のコマンドを実行：

```powershell
.\build.ps1
```

このスクリプトは以下を自動的に実行します：
1. 仮想環境の有効化
2. PyInstallerのインストール（未インストールの場合）
3. 古いビルドファイルの削除
4. PyInstallerによるEXEファイルの生成
5. ビルド結果の表示

## 手動ビルド

より細かい制御が必要な場合：

```powershell
# 仮想環境を有効化
.\venv\Scripts\Activate.ps1

# PyInstallerでビルド
pyinstaller `
    --name=NetworkAdapterSwitcher `
    --onefile `
    --windowed `
    --clean `
    --add-data="src;src" `
    --hidden-import=tkinter `
    --hidden-import=tkinter.ttk `
    --hidden-import=tkinter.messagebox `
    --manifest=app.manifest `
    src\main.py
```

## ビルドオプション説明

| オプション | 説明 |
|-----------|------|
| `--name` | 生成されるEXEファイルの名前 |
| `--onefile` | 単一の実行ファイルとして生成（依存ファイルを埋め込み） |
| `--windowed` | コンソールウィンドウを表示しない（GUIアプリ用） |
| `--clean` | ビルド前にキャッシュをクリア |
| `--add-data` | データファイルを含める |
| `--hidden-import` | 明示的にインポートするモジュールを指定 |
| `--manifest` | Windowsマニフェストファイル（管理者権限要求） |

## 生成されるファイル

ビルド成功後、以下のファイルが生成されます：

```
dist/
└── NetworkAdapterSwitcher.exe  # 実行ファイル（約12MB）

build/                           # ビルド中間ファイル（削除可能）
NetworkAdapterSwitcher.spec      # PyInstaller設定ファイル
```

## 実行ファイルの使用

生成された `NetworkAdapterSwitcher.exe` を実行する方法：

### 方法1: 右クリックメニュー（推奨）

1. `NetworkAdapterSwitcher.exe` を右クリック
2. 「管理者として実行」を選択
3. UACダイアログで「はい」をクリック

### 方法2: ショートカット作成

1. EXEファイルのショートカットを作成
2. ショートカットを右クリック → プロパティ
3. 「詳細設定」→「管理者として実行」にチェック
4. 以降、ショートカットをダブルクリックするだけで起動

### 方法3: PowerShellから実行

```powershell
Start-Process -FilePath "dist\NetworkAdapterSwitcher.exe" -Verb RunAs
```

## トラブルシューティング

### ビルドエラー

**エラー**: `ModuleNotFoundError`

**解決策**: 必要な依存パッケージがインストールされているか確認

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 実行時エラー

**エラー**: 「このアプリがデバイスに変更を加えることを許可しますか？」が表示されない

**解決策**: `app.manifest` が正しく適用されているか確認。手動で右クリック→管理者として実行してください。

**エラー**: 起動時にクラッシュする

**解決策**: 
1. `build.ps1` を実行して再ビルド
2. Windowsのウイルス対策ソフトが実行をブロックしていないか確認
3. イベントビューアーでエラーログを確認

## 配布

EXEファイル単体で配布可能です：

1. `dist\NetworkAdapterSwitcher.exe` をコピー
2. 配布先で管理者として実行

**注意事項**:
- .NET Frameworkやその他のランタイムは不要
- Python実行環境も不要
- ただし、Windows 10/11が必要
- ネットワークアダプターの制御には管理者権限が必須

## ファイルサイズを削減する場合

より小さいEXEファイルが必要な場合は、`--onefile` の代わりに `--onedir` を使用：

```powershell
pyinstaller --name=NetworkAdapterSwitcher --onedir --windowed --manifest=app.manifest src\main.py
```

この場合、`dist\NetworkAdapterSwitcher\` フォルダ全体を配布する必要があります。
