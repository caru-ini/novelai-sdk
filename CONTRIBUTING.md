# Contributing to NovelAI Python SDK

English | [日本語](/docs/CONTRIBUTING_jp.md)

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to NovelAI Python SDK. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Development Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and [poethepoet](https://github.com/nat-n/poethepoet) for task running.

1.  **Clone the repository**

    ```bash
    git clone https://github.com/caru-ini/novelai-sdk.git
    cd novelai-sdk
    ```

2.  **Install dependencies**

    ```bash
    uv sync
    ```

## Code Quality

We use several tools to ensure code quality. You can run them individually or all together using `poe`.

-   **Formatting**: We use `ruff` for code formatting.
-   **Linting**: We use `ruff` for linting.
-   **Type Checking**: We use `pyright` for static type checking.

### Running Checks

You can run the following commands using `uv run poe <task>`:

```bash
# Format code
uv run poe fmt

# Lint code
uv run poe lint

# Fix linting issues automatically where possible
uv run poe lint-fix

# Run type checking
uv run poe check

# Run all pre-commit checks (fmt, lint, check)
uv run poe pre-commit
```

## Testing

We use `pytest` for testing.

```bash
# Run tests
uv run poe test

# Run tests with coverage
uv run poe test-cov
```

Note: While tests are planned, the current test suite might be minimal. Contributions adding tests are highly appreciated.

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages. This allows us to automatically generate changelogs and determine version numbers.

**Format:**
```plaintext
<type>(<scope>): <subject>
```

**Common usage:**

-   `feat`: A new feature
-   `fix`: A bug fix
-   `docs`: Documentation only changes
-   `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
-   `refactor`: A code change that neither fixes a bug nor adds a feature
-   `perf`: A code change that improves performance
-   `test`: Adding missing tests or correcting existing tests
-   `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

**Example:**
```plaintext
feat(image): add support for new sampler
fix(api): handle timeout errors correctly
docs: update installation guide
```

## Versioning

This project uses [Semantic Versioning](https://semver.org/). The version number is automatically determined based on the commit messages using [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/).

**How commit types affect the version:**

| Commit Type                                  | Version Change             | Example                             |
| :------------------------------------------- | :------------------------- | :---------------------------------- |
| `feat`                                       | **MINOR** (0.4.2 -> 0.5.0) | `feat: add new feature`             |
| `fix`                                        | **PATCH** (0.4.2 -> 0.4.3) | `fix: fix bug`                      |
| `perf`                                       | **PATCH** (0.4.2 -> 0.4.3) | `perf: improve performance`         |
| `docs`, `style`, `refactor`, `test`, `chore` | **None** (No Release)      | `docs: update readme`               |
| `BREAKING CHANGE:` footer                    | **MAJOR** (0.4.2 -> 1.0.0) | `feat: ...\n\nBREAKING CHANGE: ...` |

## Pull Request Process

1.  Fork the repository and create your branch from `main`.
2.  If you've added code that should be tested, add tests.
3.  Ensure your code passes all quality checks (`uv run poe pre-commit`).
4.  Make sure your commit messages follow the Conventional Commits specification.
5.  Issue that Pull Request!

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
