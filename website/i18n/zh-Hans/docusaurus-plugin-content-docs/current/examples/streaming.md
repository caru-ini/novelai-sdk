# 流式生成 (Streaming Generation)

图像生成可能需要几秒到几十秒。
SSE (Server-Sent Events) 流式传输允许您实时接收生成过程。
这向用户提供反馈，表明正在发生某些事情，从而减少感知的延迟。

```python
from novelai.types import GenerateImageStreamParams
from base64 import b64decode

# 客户端初始化 (已省略)

params = GenerateImageStreamParams(
    prompt="masterpiece, best quality, scenery, detailed",
    model="nai-diffusion-4-5-full",
    stream="sse", # 启用流模式
    steps=28,
)

# 使用 generate_stream 方法
for chunk in client.image.generate_stream(params):
    if chunk.image:
        image_data = b64decode(chunk.image)
        print(f"Received chunk: {len(image_data)} bytes")
        # 您可以在此处将数据发送到前端 or 更新预览
```
