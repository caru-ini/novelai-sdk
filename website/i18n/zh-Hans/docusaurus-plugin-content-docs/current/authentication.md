---
sidebar_position: 3
title: 认证
---

# 认证

您需要进行认证才能使用 NovelAI API。
`novelai-sdk` 支持标准的认证方法。

## 环境变量（推荐）

强烈建议使用环境变量，而不是硬编码 API 密钥。

在您的环境中设置 `NOVELAI_API_KEY`：

```bash
export NOVELAI_API_KEY="pst-..."
```

Python 代码：

```python
from novelai import NovelAI

# 自动读取环境变量
client = NovelAI()
```

## .env 文件

使用 `.env` 文件和 `python-dotenv` 也是常见的做法。

`.env`:
```env
NOVELAI_API_KEY=pst-your-api-key-here
```

Python 代码：
```python
from dotenv import load_dotenv
from novelai import NovelAI

load_dotenv()
client = NovelAI()
```

## 直接初始化

用于脚本或测试：

```python
from novelai import NovelAI

client = NovelAI(api_key="pst-your-api-key-here")
```
