# GitHubセットアップガイド

このドキュメントでは、プロジェクトをGitHubにアップロードし、CI/CDを有効化する手順を説明します。

## 前提条件

- GitHubアカウントを持っていること
- Gitがインストールされていること
- プロジェクトのローカルコピーがあること

## 手順

### 1. Gitリポジトリの初期化

プロジェクトルートで以下を実行：

```powershell
# Gitリポジトリを初期化（未実施の場合）
git init

# .gitignoreが正しく設定されていることを確認
cat .gitignore

# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: Network Adapter Switcher v1.0.1"
```

### 2. GitHubリポジトリの作成

1. GitHubにログイン
2. 右上の「+」→「New repository」をクリック
3. リポジトリ情報を入力：
   - **Repository name**: `net-adaptor-change`
   - **Description**: `WindowsでイーサネットとWi-Fiアダプターを排他的に切り替えるGUIツール`
   - **Public** または **Private** を選択
   - **README**, **.gitignore**, **license** は追加しない（既に存在するため）
4. 「Create repository」をクリック

### 3. リモートリポジトリの設定

GitHubに表示されるコマンドを実行：

```powershell
# リモートリポジトリを追加（ユーザー名を自分のものに変更）
git remote add origin https://github.com/UserName/net-adaptor-change.git

# メインブランチを設定
git branch -M main

# プッシュ
git push -u origin main
```

### 4. GitHub Actions の有効化

プッシュ後、自動的にGitHub Actionsが有効になります：

1. GitHubリポジトリの「Actions」タブを開く
2. 最初のワークフロー実行が開始されることを確認
3. CI実行結果を確認

### 5. リポジトリ設定

#### 5.1 ブランチ保護ルール（推奨）

1. 「Settings」→「Branches」
2. 「Add rule」をクリック
3. Branch name pattern: `main`
4. 以下を有効化：
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
     - 必須チェック: `Code Quality & Tests`
   - ✅ Require conversation resolution before merging
   - ✅ Do not allow bypassing the above settings
5. 「Create」をクリック

#### 5.2 Discussions の有効化（推奨）

1. 「Settings」→「General」
2. 「Features」セクション
3. ✅ Discussions を有効化

#### 5.3 Security の設定

1. 「Settings」→「Security」
2. 「Code security and analysis」
3. 以下を有効化：
   - ✅ Dependency graph
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates

### 6. 最初のリリースを作成

#### オプション1: 手動リリース

1. 「Releases」→「Create a new release」
2. Tag version: `v1.0.1`
3. Release title: `v1.0.1`
4. Description: 変更内容を記載
5. EXEファイルをアップロード
6. 「Publish release」

#### オプション2: 自動リリース（推奨）

タグをプッシュすると自動的にリリースが作成されます：

```powershell
# タグを作成
git tag -a v1.0.1 -m "Release v1.0.1"

# タグをプッシュ
git push origin v1.0.1
```

数分後、以下が自動的に実行されます：
1. コード品質チェック
2. EXEファイルのビルド
3. GitHubリリースの作成
4. 成果物のアップロード

「Actions」タブで進捗を確認できます。

### 7. READMEバッジの更新

README.mdのバッジURLを実際のリポジトリURLに更新：

```powershell
# README.mdを編集
# UserName を自分のGitHubユーザー名に変更
```

```markdown
[![CI](https://github.com/YourUsername/net-adaptor-change/actions/workflows/ci.yml/badge.svg)](https://github.com/YourUsername/net-adaptor-change/actions/workflows/ci.yml)
```

変更をコミット＆プッシュ：

```powershell
git add README.md
git commit -m "docs: Update README badges with actual repository URL"
git push
```

### 8. Codecov の設定（オプション）

コードカバレッジを可視化したい場合：

1. [Codecov](https://codecov.io/)にGitHubアカウントでログイン
2. リポジトリを追加
3. トークンをコピー（パブリックリポジトリの場合は不要）
4. リポジトリの「Settings」→「Secrets and variables」→「Actions」
5. 「New repository secret」
   - Name: `CODECOV_TOKEN`
   - Value: コピーしたトークン

## 開発ワークフロー

### 新機能の開発

```powershell
# 新しいブランチを作成
git checkout -b feature/your-feature

# 開発＆コミット
git add .
git commit -m "[FEAT] Add new feature"

# プッシュ
git push -u origin feature/your-feature

# GitHubでプルリクエストを作成
```

### バグ修正

```powershell
# 修正ブランチを作成
git checkout -b fix/bug-description

# 修正＆コミット
git add .
git commit -m "[FIX] Fix bug description"

# プッシュ＆プルリクエスト
git push -u origin fix/bug-description
```

### 新バージョンのリリース

```powershell
# 1. mainブランチで最新を取得
git checkout main
git pull origin main

# 2. CHANGELOG.mdを更新
# [Unreleased] → [1.0.2] に変更

# 3. コミット
git add CHANGELOG.md
git commit -m "chore: Prepare release v1.0.2"
git push

# 4. タグを作成＆プッシュ
git tag -a v1.0.2 -m "Release v1.0.2"
git push origin v1.0.2

# 自動的にリリースワークフローが実行されます
```

## トラブルシューティング

### GitHub Actionsが失敗する

1. 「Actions」タブでエラーログを確認
2. ローカルで再現：
   ```powershell
   mypy src/
   ruff check src/
   black --check src/
   pytest tests/
   ```

### プッシュが拒否される

```powershell
# 最新をプル
git pull origin main --rebase

# 再度プッシュ
git push
```

### タグを削除したい

```powershell
# ローカルのタグを削除
git tag -d v1.0.1

# リモートのタグを削除
git push origin --delete v1.0.1
```

## 参考資料

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [GitHub Releases Documentation](https://docs.github.com/repositories/releasing-projects-on-github)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

---

セットアップに問題がある場合は、[Discussions](https://github.com/UserName/net-adaptor-change/discussions)で質問してください。
