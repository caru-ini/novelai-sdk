# 图生图 (Image-to-Image / i2i)

基于现有图像生成新图像。
用于细化草图或改变图像风格。

```python
from novelai.types import GenerateImageParams, I2iParams

# 配置 i2i 参数
i2i_params = I2iParams(
    image="input_sketch.png",  # Base64 字符串或文件路径
    # 改变强度
    # 接近 0.0: 保持原始图像
    # 接近 1.0: 侧重于提示词，偏离原始图像
    strength=0.7,
    noise=0.0,
)

params = GenerateImageParams(
    prompt="cyberpunk style, neon lights, highly detailed",
    model="nai-diffusion-4-5-full",
    i2i=i2i_params,
)

# 生成方式是标准的
# images = client.image.generate(params)
```
