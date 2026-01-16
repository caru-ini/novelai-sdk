# 角色参考 (Character Reference)

使用参考图像保持一致的角色外观。
当您想在不同情况下生成同一角色时，这非常有用。

```python
from novelai.types import CharacterReference, GenerateImageParams

# 定义参考
character_references = [
    CharacterReference(
        image="reference.png", # Base64 字符串或文件路径
        type="character",
        fidelity=0.75, # 强度 (0.0 到 1.0)
    )
]

# 配置生成
params = GenerateImageParams(
    prompt="1girl, standing in a garden",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)

# 执行 (假设客户端已初始化)
# images = client.image.generate(params)
```
