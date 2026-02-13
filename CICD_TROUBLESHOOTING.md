# CI/CD トラブルシューティング

このドキュメントでは、GitHub Actionsで発生する一般的な問題と解決方法を説明します。

## 目次

- [マニフェストファイルが見つからない](#マニフェストファイルが見つからない)
- [PyInstallerビルドエラー](#pyinstallerビルドエラー)
- [テスト失敗](#テスト失敗)
- [権限エラー](#権限エラー)

## マニフェストファイルが見つからない

### 問題

```
FileNotFoundError: [Errno 2] No such file or directory: 'app.manifest'
```

### 原因

GitHub Actionsの実行環境で相対パスが正しく解決されない場合があります。

### 解決方法

**修正済み**: ワークフローファイルで絶対パスを使用するように修正しました。

```yaml
- name: Verify manifest file
  run: |
    if (Test-Path "app.manifest") {
      Write-Host "✓ app.manifest found"
    } else {
      Write-Host "✗ app.manifest not found"
      exit 1
    }

- name: Build EXE
  run: |
    $manifestPath = Join-Path $PWD "app.manifest"
    pyinstaller --manifest="$manifestPath" ...
```

### 手動確認方法

ローカルでビルドする場合は問題ありませんが、GitHub Actionsでエラーが出る場合：

1. `app.manifest`ファイルがリポジトリにコミットされているか確認
2. `.gitignore`で除外されていないか確認

```powershell
git ls-files app.manifest
```

ファイルが表示されればOKです。

## PyInstallerビルドエラー

### 問題

```
ModuleNotFoundError: No module named 'xxx'
```

### 解決方法

1. **隠しインポートの追加**

   ワークフローファイルに`--hidden-import`を追加：

   ```yaml
   --hidden-import=module_name
   ```

2. **依存関係の確認**

   `requirements.txt`に必要なパッケージが含まれているか確認：

   ```powershell
   pip install -r requirements.txt
   pip list
   ```

## テスト失敗

### 型チェックエラー (mypy)

```
error: Incompatible types
```

**解決方法:**

1. ローカルで型チェックを実行：

   ```powershell
   mypy src/
   ```

2. 型ヒントを修正

3. 型無視が必要な場合（最終手段）：

   ```python
   # type: ignore
   ```

### リンターエラー (ruff)

```
E501 Line too long
```

**解決方法:**

1. 自動修正を試す：

   ```powershell
   ruff check --fix src/
   ```

2. 手動で修正

### フォーマットエラー (black)

```
would reformat file.py
```

**解決方法:**

```powershell
black src/
```

### テストエラー (pytest)

```
FAILED tests/test_xxx.py::test_function
```

**解決方法:**

1. ローカルでテストを実行：

   ```powershell
   pytest tests/ -v
   ```

2. 失敗したテストを確認して修正

3. モックが正しく設定されているか確認

## 権限エラー

### 問題

```
PermissionError: [Errno 13] Permission denied
```

### 解決方法

GitHub Actionsでは管理者権限は不要です（ビルドのみ実行）。

もしローカルでエラーが出る場合：

```powershell
# PowerShellを管理者として実行
```

## アーティファクトアップロードエラー

### 問題

```
Error: Unable to find any artifacts
```

### 解決方法

1. ビルドステップが成功しているか確認
2. `dist/NetworkAdapterSwitcher.exe`が存在するか確認

   ```yaml
   - name: Verify build
     run: |
       if (Test-Path "dist\NetworkAdapterSwitcher.exe") {
         Write-Host "✓ EXE exists"
       } else {
         Write-Host "✗ EXE not found"
         exit 1
       }
   ```

## リリースワークフローエラー

### 問題

```
Error: Resource not accessible by integration
```

### 原因

GITHUB_TOKENの権限が不足しています。

### 解決方法

リポジトリ設定を確認：

1. Settings → Actions → General
2. "Workflow permissions"
3. "Read and write permissions"を選択
4. "Allow GitHub Actions to create and approve pull requests"にチェック
5. 保存

## Codecov エラー

### 問題

```
Error uploading coverage reports
```

### 解決方法

**オプション機能**: Codecovは必須ではありません。

失敗しても無視するように設定済み：

```yaml
fail_ci_if_error: false
```

Codecovを有効化したい場合：

1. [Codecov](https://codecov.io/)でリポジトリを連携
2. トークンを取得（公開リポジトリの場合は不要）
3. リポジトリシークレットに追加：
   - Name: `CODECOV_TOKEN`
   - Value: トークン

## デバッグ方法

### ワークフローログの確認

1. GitHubリポジトリの「Actions」タブ
2. 失敗したワークフローをクリック
3. 失敗したジョブをクリック
4. 各ステップのログを展開して確認

### ローカルでの再現

```powershell
# CIと同じチェックを実行
.\venv\Scripts\Activate.ps1
mypy src/
ruff check src/
black --check src/
pytest tests/

# ビルドテスト
.\build.ps1
```

### デバッグモードの有効化

ワークフローファイルに以下を追加：

```yaml
- name: Debug info
  run: |
    Write-Host "Working directory: $PWD"
    Write-Host "Files:"
    Get-ChildItem -Recurse -File | Select-Object FullName
```

## よくある質問

### Q: CIが遅い

**A:** マトリックステストを減らすか、キャッシュを有効化（既に設定済み）：

```yaml
- uses: actions/setup-python@v5
  with:
    cache: 'pip'  # ← これがキャッシュを有効化
```

### Q: 特定のPythonバージョンでのみ失敗する

**A:** そのバージョンでのみ発生する互換性問題があります。

1. ローカルでそのバージョンをインストールして確認
2. 必要に応じてコードを修正
3. またはそのバージョンをマトリックスから除外

### Q: リリースが自動作成されない

**A:** タグの形式を確認：

```powershell
# 正しい形式
git tag -a v1.0.0 -m "Release v1.0.0"

# 間違った形式
git tag 1.0.0  # vプレフィックスなし
git tag release-1.0.0  # 形式が違う
```

## サポート

問題が解決しない場合：

1. [GitHub Issues](https://github.com/roflsunriz/network-adaptor-switcher/issues)で報告
2. [Discussions](https://github.com/roflsunriz/network-adaptor-switcher/discussions)で質問
3. ワークフローログを添付してください

---

このドキュメントは随時更新されます。新しい問題が見つかった場合は追記してください。
