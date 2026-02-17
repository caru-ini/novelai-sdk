# 局部重绘 (Inpainting)

重新生成现有图像中被遮罩覆盖的区域。
使用遮罩图像指定需要重新生成的部分，其余部分保持不变。

## 基本示例

```python
from novelai.types import GenerateImageParams, InpaintParams

inpaint_params = InpaintParams(
    image="source.png",   # 源图像（文件路径、Base64 或 PIL Image）
    mask="mask.png",      # 遮罩图像（白色=重绘、黑色=保留）
    strength=1.0,
)

# 模型会自动切换到局部重绘变体
# (例如 nai-diffusion-4-5-full -> nai-diffusion-4-5-full-inpainting)
params = GenerateImageParams(
    prompt="1girl, standing, smile",
    model="nai-diffusion-4-5-full",
    inpaint=inpaint_params,
)

# images = client.image.generate(params)
```

## 遮罩格式

遮罩图像用于指定需要重新生成的区域：

- **白色** (`#FFFFFF`): 需要重新生成的区域（重绘）
- **黑色** (`#000000`): 保持不变的区域

遮罩会自动进行预处理（二值化和缩放）以满足 API 要求。

## 参数

- **`image`**（必需）: 源图像（文件路径、Base64 字符串或 PIL Image）
- **`mask`**（必需）: 定义重绘区域的遮罩图像（文件路径、Base64 字符串或 PIL Image）
- **`strength`**: 重绘强度（`0.01`–`1.0`，默认: `1.0`）
  - `1.0`: 完全重新生成遮罩区域
  - 较低值: 将原始内容与新生成内容混合
- **`seed`**: 噪声随机种子（省略时自动生成）

:::info
模型会自动切换到局部重绘变体（例如 `nai-diffusion-4-5-full` → `nai-diffusion-4-5-full-inpainting`）。无需手动指定重绘模型。
:::

:::tip
为了获得最佳效果，遮罩应略大于你想要更改的区域。这样可以为模型提供更多上下文，实现无缝融合。
:::
