# 多角色定位 (Multi-Character Positioning)

生成多个角色时，他们的特征（发色、瞳色、衣服）有时会混合在一起。
多角色定位允许您为每个角色分配特定的提示词和位置，从而防止此问题。

```python
from novelai.types import Character, GenerateImageParams

characters = [
    Character(
        prompt="1girl, red hair, blue eyes, school uniform",
        enabled=True,
        position=(0.2, 0.5), # 左 (X: 0.2, Y: 0.5)
    ),
    Character(
        prompt="1boy, black hair, green eyes, casual clothes",
        enabled=True,
        position=(0.8, 0.5), # 右 (X: 0.8, Y: 0.5)
    ),
]

params = GenerateImageParams(
    # 可以使用通用提示词，但细节应在 characters 列表中
    prompt="two people standing together, holding hands, best quality",
    model="nai-diffusion-4-5-full",
    size=(832, 1216),  # 必须明确指定尺寸
    characters=characters,
)
```
