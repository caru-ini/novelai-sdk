# NovelAI Python SDK への貢献

[English](/CONTRIBUTING.md) | 日本語

貢献をご検討いただきありがとうございます！

以下は、NovelAI Python SDK に貢献するためのガイドラインです。これらはあくまでガイドラインであり、絶対的なルールではありません。最善の判断を行い、必要であればこのドキュメントへの変更をプルリクエストで提案してください。

## 開発環境のセットアップ
このプロジェクトでは、依存関係の管理に [uv](https://github.com/astral-sh/uv)、タスクランナーに [poethepoet](https://github.com/nat-n/poethepoet) を使用しています。

1.  **リポジトリのクローン**

    ```bash
    git clone https://github.com/caru-ini/novelai-sdk.git
    cd novelai-sdk
    ```

2.  **依存関係のインストール**

    ```bash
    uv sync
    ```

## コード品質

コード品質を保つためにいくつかのツールを使用しています。これらは個別に実行することも、`poe` を使ってまとめて実行することもできます。

-   **フォーマット**: コードの整形には `ruff` を使用しています。
-   **Lint**: 静的解析には `ruff` を使用しています。
-   **型チェック**: 静的型チェックには `pyright` を使用しています。

### チェックの実行

以下のコマンドは `uv run poe <task>` で実行できます：

```bash
# コードのフォーマット
uv run poe fmt

# Lint の実行
uv run poe lint

# 可能な場合、Lint の問題を自動修正
uv run poe lint-fix

# 型チェックの実行
uv run poe check

# コミット前の全チェック実行 (fmt, lint, check)
uv run poe pre-commit
```

## テスト

テストには `pytest` を使用しています。

```bash
# テストの実行
uv run poe test

# カバレッジ付きでテストを実行
uv run poe test-cov
```

注意：テストの追加は計画中であり、現在のテストスイートは最小限である可能性があります。テストを追加する貢献は大歓迎です。

## コミットガイドライン

コミットメッセージには [Conventional Commits](https://www.conventionalcommits.org/ja/v1.0.0/) を採用しています。これにより、変更履歴の自動生成やバージョン番号の決定が可能になります。

**フォーマット:**
```plaintext
<種類>(<スコープ>): <主な変更内容(英語で)>
```

**主な種類:**

-   `feat`: 新機能
-   `fix`: バグ修正
-   `docs`: ドキュメントのみの変更
-   `style`: コードの意味に影響しない変更（空白、フォーマットなど）
-   `refactor`: バグ修正も機能追加も行わないコードの変更
-   `perf`: パフォーマンスを向上させるコードの変更
-   `test`: 不足しているテストの追加や既存のテストの修正
-   `chore`: ビルドプロセスやドキュメント生成などの補助ツールやライブラリの変更

**例:**
```plaintext
feat(image): add support for new sampler
fix(api): handle timeout errors correctly
docs: update installation guide
```

## バージョニング (Versioning)

このプロジェクトでは [Semantic Versioning](https://semver.org/) を採用しています。バージョン番号は、[python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/) を使用してコミットメッセージに基づいて自動的に決定されます。

**コミットの種類とバージョンの変化:**

| コミットの種類 (Type)                        | バージョンの変化           | 例                                               |
| :------------------------------------------- | :------------------------- | :----------------------------------------------- |
| `feat`                                       | **MINOR** (0.4.2 -> 0.5.0) | `feat: 新機能を追加`                             |
| `fix`                                        | **PATCH** (0.4.2 -> 0.4.3) | `fix: バグを修正`                                |
| `perf`                                       | **PATCH** (0.4.2 -> 0.4.3) | `perf: パフォーマンス改善`                       |
| `docs`, `style`, `refactor`, `test`, `chore` | **なし** (リリースなし)    | `docs: READMEを更新`                             |
| `BREAKING CHANGE:` フッター                  | **MAJOR** (0.4.2 -> 1.0.0) | `feat: ...\n\nBREAKING CHANGE: APIの仕様変更...` |

## プルリクエストの手順

1.  リポジトリをフォークし、`main` からブランチを作成してください。
2.  テストが必要なコードを追加した場合は、テストを追加してください。
3.  コードがすべての品質チェックに合格することを確認してください (`uv run poe pre-commit`)。
4.  コミットメッセージが Conventional Commits の仕様に従っているか確認してください。
5.  プルリクエストを送信してください！

## ライセンス

貢献することにより、あなたの貢献が MIT ライセンスの下でライセンスされることに同意したものとみなされます。
