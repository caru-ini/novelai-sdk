# 图生图 (Image-to-Image / i2i)

基于现有图像生成新图像。
用于细化草图或改变图像风格。

## 基本示例

```python
from novelai.types import GenerateImageParams, I2iParams

# 配置 i2i 参数
i2i_params = I2iParams(
    image="input_sketch.png",  # Base64 字符串或文件路径
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

## 参数

- **`image`**（必需）: 源图像（文件路径、Base64 字符串或 PIL Image）
- **`strength`**: 输出偏离源图像的程度（`0.01`–`0.99`，默认: `0.7`）
  - 接近 `0.0`: 保持原始图像
  - 接近 `1.0`: 侧重于提示词，偏离原始图像
- **`noise`**: 用于变化的噪声注入量（`0.0`–`0.99`，默认: `0.0`）
- **`seed`**: 噪声随机种子（省略时自动生成）

:::tip
建议从 `strength=0.5` 开始，根据你想改变原始图像的程度进行调整。
:::
