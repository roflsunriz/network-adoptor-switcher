# ネットワークアダプター切り替えツール

WindowsでイーサネットとWi-Fiアダプターを排他的に切り替えるGUIツールです。

## 概要

Windows PCにイーサネットとWi-Fiが接続されている場合、通常はイーサネットが優先されます。このツールを使用すると、簡単にイーサネットとWi-Fiを切り替えることができます。

### 主な機能

- イーサネットアダプターとWi-Fiアダプターの自動検出
- ワンクリックでアダプターを排他的に切り替え
- アダプターの状態をリアルタイム表示
- 管理者権限チェック

## 必要な環境

- Windows 10/11
- Python 3.10以降
- 管理者権限（ネットワークアダプターの有効/無効化のため）

## 環境構築

### 1. リポジトリのクローンまたはダウンロード

```powershell
cd C:\Users\UserName\Documents
# または任意のディレクトリ
```

### 2. 仮想環境の作成

```powershell
python -m venv venv
```

### 3. 仮想環境の有効化

```powershell
.\venv\Scripts\Activate.ps1
```

PowerShellの実行ポリシーでエラーが出る場合：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. 依存パッケージのインストール

```powershell
pip install -r requirements.txt
```

## 使用方法

### アプリケーションの起動

**重要**: 管理者権限で実行する必要があります。

#### 方法1: PowerShellから管理者として実行

```powershell
# PowerShellを管理者として起動してから
cd C:\Users\UserName\Documents\net-adaptor-change
.\venv\Scripts\Activate.ps1
python src/main.py
```

#### 方法2: ショートカットを作成（推奨）

1. `src/main.py` を右クリック → 「ショートカットの作成」
2. ショートカットを右クリック → 「プロパティ」
3. 「ショートカット」タブ → 「詳細設定」→ 「管理者として実行」にチェック
4. 「リンク先」を以下のように編集：
   ```
   C:\Users\UserName\Documents\net-adaptor-change\venv\Scripts\pythonw.exe "C:\Users\UserName\Documents\net-adaptor-change\src\main.py"
   ```
5. 「作業フォルダー」を設定：
   ```
   C:\Users\UserName\Documents\net-adaptor-change
   ```

### 操作方法

1. アプリケーションを起動すると、現在のアダプター状態が表示されます
2. 「イーサネットに切り替え」ボタン：Wi-Fiを無効化してイーサネットを有効化
3. 「Wi-Fiに切り替え」ボタン：イーサネットを無効化してWi-Fiを有効化
4. 「状態を更新」ボタン：アダプター情報を最新の状態に更新

## 実行ファイル（EXE）のビルド

### クイックビルド

PowerShellスクリプトを使用して簡単にビルドできます：

```powershell
.\build.ps1
```

ビルドが成功すると、`dist\NetworkAdapterSwitcher.exe` が生成されます（約12MB）。

生成されたEXEファイルを右クリック → 「管理者として実行」で起動してください。

詳細なビルド手順とオプションについては、[BUILD.md](BUILD.md)を参照してください。

## 開発者向け

### コード品質チェック

#### 型チェック

```powershell
mypy src/
```

#### リンターチェック

```powershell
ruff check src/
```

#### フォーマットチェック

```powershell
black --check src/
```

#### 自動フォーマット

```powershell
black src/
ruff check --fix src/
```

### テスト実行

```powershell
pytest tests/
```

カバレッジレポート付き：

```powershell
pytest --cov=src --cov-report=html
```

### プロジェクト構造

```
net-adaptor-change/
├── src/
│   ├── __init__.py
│   ├── main.py              # エントリーポイント
│   ├── network_manager.py   # ネットワークアダプター管理
│   ├── gui.py               # GUI実装
│   └── models/
│       ├── __init__.py
│       └── models.py        # 型定義
├── tests/                   # テストコード
├── requirements.txt         # 依存パッケージ
├── pyproject.toml          # プロジェクト設定
├── .gitignore              # Git除外設定
├── .env.example            # 環境変数例
└── README.md               # このファイル
```

## トラブルシューティング

### 管理者権限エラー

**エラー**: 「このアプリケーションは管理者権限で実行する必要があります」

**解決策**: PowerShellまたはアプリケーションを管理者として実行してください。

### アダプターが見つからない

**エラー**: 「イーサネットアダプターが見つかりません」または「Wi-Fiアダプターが見つかりません」

**解決策**: 
1. デバイスマネージャーでアダプターが認識されているか確認
2. アダプターの名前やインターフェース説明を確認
3. 必要に応じて `src/network_manager.py` の `_parse_adapter_type` メソッドを調整

### PowerShellコマンド実行エラー

**エラー**: 「PowerShellコマンド実行エラー」

**解決策**:
1. PowerShellが正しくインストールされているか確認
2. `Get-NetAdapter` コマンドが手動で実行できるか確認
3. 実行ポリシーを確認：`Get-ExecutionPolicy`

## ログファイル

アプリケーションの動作ログは `network_adapter_switcher.log` に保存されます。

## ライセンス

MIT License

## 作成者

- 作成日：2026年2月14日
- バージョン：1.0.0
