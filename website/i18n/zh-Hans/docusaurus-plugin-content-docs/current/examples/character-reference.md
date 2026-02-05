# 精密参考 (Precision Reference)

:::info
此功能以前称为"角色参考 (Character Reference)"，于2026年2月更名为"精密参考"。
:::

使用参考图像控制角色外观和艺术风格。
精密参考允许您在多次生成中保持一致的角色设计，并应用特定的艺术风格。

## 主要功能

- **多图片支持**: 组合多个参考以应用不同的角色和风格
- **参考类型**:
  - `"character"`: 仅参考角色外观
  - `"style"`: 仅参考艺术风格
  - `"character&style"`: 同时参考角色和风格（默认）
- **精细控制**: 为每个参考调整fidelity和strength

## 基本示例

```python
from novelai.types import CharacterReference, GenerateImageParams

# 单个角色参考
character_references = [
    CharacterReference(
        image="reference.png",  # Base64 字符串或文件路径
        type="character",  # "character", "style", 或 "character&style"
        fidelity=1.0,  # 参考忠实度 (0.0 到 1.0，默认: 1.0)
        strength=1.0,  # 参考权重 (0.0 到 1.0，默认: 1.0)
    )
]

params = GenerateImageParams(
    prompt="1girl, standing in a garden",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)

# 执行 (假设客户端已初始化)
# images = client.image.generate(params)
```

## 高级用法: 多个参考

从不同图像组合角色和风格参考：

```python
character_references = [
    CharacterReference(
        image="character.png",
        type="character",  # 仅角色外观
        fidelity=1.0,
        strength=0.75,
    ),
    CharacterReference(
        image="style.png",
        type="style",  # 仅艺术风格
        fidelity=1.0,
        strength=0.75,
    ),
]

params = GenerateImageParams(
    prompt="1girl, standing, rating:general, very aesthetic",
    model="nai-diffusion-4-5-full",
    character_references=character_references,
)
```

## 参数说明

- **`image`**（必需）: 参考图像（文件路径、Base64字符串或PIL Image）
- **`type`**: 参考类型
  - `"character"`: 仅应用角色外观
  - `"style"`: 仅应用艺术风格
  - `"character&style"`: 同时应用两者（默认）
- **`fidelity`**: 与参考的匹配度 (0.0-1.0，默认: 1.0)
- **`strength`**: 使用多个参考时的相对权重 (0.0-1.0，默认: 1.0)
