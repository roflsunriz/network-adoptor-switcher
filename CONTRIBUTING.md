# コントリビューションガイド

このプロジェクトへの貢献に興味を持っていただき、ありがとうございます！

## 行動規範

このプロジェクトに参加するすべての人は、敬意を持って他者と接することが期待されます。

## 貢献方法

### バグ報告

バグを発見した場合：

1. [Issues](https://github.com/UserName/net-adaptor-change/issues)で既存の報告を検索
2. 見つからない場合、[バグ報告テンプレート](https://github.com/UserName/net-adaptor-change/issues/new?template=bug_report.md)を使用して新しいIssueを作成

### 機能提案

新機能を提案する場合：

1. [Issues](https://github.com/UserName/net-adaptor-change/issues)で既存の提案を検索
2. [機能要望テンプレート](https://github.com/UserName/net-adaptor-change/issues/new?template=feature_request.md)を使用して新しいIssueを作成
3. コミュニティからのフィードバックを待つ

### プルリクエスト

#### 事前準備

1. **Issueを作成**: 大きな変更の場合、まずIssueで議論してください
2. **フォーク**: このリポジトリをフォークします
3. **ブランチ作成**: `git checkout -b feature/your-feature-name`

#### 開発環境のセットアップ

```powershell
# 1. リポジトリをクローン
git clone https://github.com/your-username/net-adaptor-change.git
cd net-adaptor-change

# 2. 仮想環境を作成
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. 依存関係をインストール
pip install -r requirements.txt
```

#### コード品質基準

すべてのコードは以下のチェックに合格する必要があります：

```powershell
# 型チェック
mypy src/

# リンター
ruff check src/

# フォーマット
black src/

# テスト
pytest tests/
```

#### コミットメッセージ

明確で説明的なコミットメッセージを書いてください：

```
[タイプ] 簡潔な説明

詳細な説明（必要に応じて）

- 変更点1
- 変更点2
```

**タイプの例:**
- `[FEAT]` - 新機能
- `[FIX]` - バグ修正
- `[DOCS]` - ドキュメント更新
- `[STYLE]` - コードフォーマット
- `[REFACTOR]` - リファクタリング
- `[TEST]` - テスト追加/修正
- `[CHORE]` - その他の変更

#### プルリクエストの作成

1. **変更をプッシュ**: `git push origin feature/your-feature-name`
2. **PRを作成**: GitHubでプルリクエストを作成
3. **テンプレートに従う**: PRテンプレートのすべてのセクションに記入
4. **CIをパス**: すべての自動チェックが成功することを確認

#### レビュープロセス

1. メンテナーがコードをレビューします
2. フィードバックに対応してください
3. 承認後、メンテナーがマージします

## 開発ガイドライン

### コーディング規約

- **型ヒント**: すべての関数に型ヒントを付ける
- **any禁止**: `any`型は使用しない
- **Docstring**: すべての公開関数にdocstringを記載
- **命名**: 変数名は明確で説明的に

### テスト

- 新機能には必ずテストを追加
- テストカバレッジは90%以上を維持
- モックを適切に使用

### ドキュメント

- READMEを更新（該当する場合）
- CHANGELOG.mdに変更を記録
- 複雑なロジックにはコメントを追加

## プロジェクト構造

```
net-adaptor-change/
├── src/
│   ├── main.py              # エントリーポイント
│   ├── network_manager.py   # ネットワーク管理
│   ├── gui.py               # GUI実装
│   └── models/
│       └── models.py        # 型定義
├── tests/                   # テストコード
├── .github/
│   ├── workflows/           # CI/CD
│   └── ISSUE_TEMPLATE/      # Issueテンプレート
├── requirements.txt         # 依存パッケージ
├── pyproject.toml          # プロジェクト設定
└── README.md               # プロジェクト説明
```

## 質問がある場合

- [Discussions](https://github.com/UserName/net-adaptor-change/discussions)で質問してください
- [Issues](https://github.com/UserName/net-adaptor-change/issues)で既存の議論を確認

## ライセンス

このプロジェクトに貢献することで、あなたの貢献がMITライセンスの下でライセンスされることに同意したことになります。

---

ご協力ありがとうございます！ 🎉
