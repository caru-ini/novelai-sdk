---
sidebar_position: 5
title: 开发 (Development)
---

# 开发 (Development)

设置开发环境。

## 先决条件
- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/) (或使用 `pip` 管理依赖)

## 安装

1. 克隆仓库：
    ```bash
    git clone https://github.com/caru-ini/novelai-sdk.git
    cd novelai-sdk
    ```

2. 安装依赖：
    ```bash
    poetry install
    ```

## 代码质量

我们要保持高代码质量。
提交前请运行以下命令。

### 格式化
使用 ruff 格式化代码。
```bash
poetry run ruff format .
```

### Linting
使用 ruff 检查 lint 问题。
```bash
poetry run ruff check . --fix
```

### 类型检查
使用 pyright 进行静态类型检查。
```bash
poetry run pyright
```

## 测试

运行测试以确保一切正常。
*注意：某些测试可能需要 API 密钥。*

```bash
poetry run pytest
```

## 贡献

1.  Fork 仓库
2.  创建功能分支 (`git checkout -b feature/amazing-feature`)
3.  提交更改 (`git commit -m 'Add some amazing feature'`)
4.  推送到分支 (`git push origin feature/amazing-feature`)
5.  开启 Pull Request

## 许可证

MIT License.
