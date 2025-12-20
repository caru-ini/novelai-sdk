---
sidebar_position: 3
title: Authentication
---

# Authentication

You need to authenticate to use the NovelAI API.
`novelai-sdk` supports standard authentication methods.

## Environment Variable (Recommended)

It is strongly recommended to use environment variables instead of hardcoding API keys.

Set `NOVELAI_API_KEY` in your environment:

```bash
export NOVELAI_API_KEY="pst-..."
```

Python code:

```python
from novelai import NovelAI

# Automatically reads the env var
client = NovelAI()
```

## .env File

Using `.env` files with `python-dotenv` is also common.

`.env`:
```env
NOVELAI_API_KEY=pst-your-api-key-here
```

Python code:
```python
from dotenv import load_dotenv
from novelai import NovelAI

load_dotenv()
client = NovelAI()
```

## Direct Initialization

For scripts or testing:

```python
from novelai import NovelAI

client = NovelAI(api_key="pst-your-api-key-here")
```
