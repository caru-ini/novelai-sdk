---
sidebar_position: 2
title: 快速开始
---

# 快速开始 (Getting Started)

了解如何使用 Python 和 NovelAI SDK 轻松生成图像。
本指南将逐步带您完成整个过程。

## 安装

需要 Python 3.10 或更高版本。

使用 pip 安装：

```bash
pip install novelai-sdk
```

或者使用 poetry：

```bash
poetry add novelai-sdk
```

## API 密钥设置

要使用 API，你需要一个 API 密钥。

1.  登录 [NovelAI](https://novelai.net/)。
2.  前往 **Settings (齿轮图标) -> Account**。
3.  点击 **Get API Key**。

我们强烈建议使用环境变量来管理你的 API 密钥：

```bash
export NOVELAI_API_KEY="pst-..."
```

SDK 会自动检测此环境变量。

## 基本用法：图像生成

这是一个生成图像的简单示例。

```python
import os
from novelai import NovelAI
from novelai.types import GenerateImageParams

# 如果你没有设置环境变量，可以直接传递 api_key="pst-..."
client = NovelAI()

# 定义参数
params = GenerateImageParams(
    prompt="1girl, cat ears, maid, cute, best quality",
    model="nai-diffusion-4-5-full",
    size=(832, 1216),
)

# 生成图像
# 返回 (image_bytes, metadata) 的列表
images = client.image.generate(params)

# 即使只请求了一张图像，它也会返回一个列表
if images:
    # 第一个元素是 PIL Image 对象
    image = images[0]
    
    # 保存图像
    image.save("output.png")
    print("图像已保存为 output.png")
```

## 异步用法

对于 web 应用程序或高性能脚本，请使用 `AsyncNovelAI`。

```python
import asyncio
from novelai import AsyncNovelAI
from novelai.types import GenerateImageParams

async def main():
    async with AsyncNovelAI() as client:
        params = GenerateImageParams(
            prompt="1boy, holding a sword, fantasy",
            model="nai-diffusion-4-5-full",
        )
        
        images = await client.image.generate(params)
        
        if images:
            images[0].save("async_output.png")

if __name__ == "__main__":
    asyncio.run(main())
```

## 错误处理

SDK 使用 Pydantic 进行验证。如果参数无效，将引发 `ValidationError`。
API 错误将引发 `NovelAIError` 或其子类。

```python
from novelai.exceptions import NovelAIError
from pydantic import ValidationError

try:
    client.image.generate(params)
except ValidationError as e:
    print(f"验证错误: {e}")
except NovelAIError as e:
    print(f"API 错误: {e}")
```
