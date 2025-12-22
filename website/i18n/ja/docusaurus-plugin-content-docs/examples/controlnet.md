# ControlNet (Vibe Transfer)

ControlNet（NovelAIではVibe TransferやPalette Transferなども含みます）を使用すると、
リファレンス画像から構図、ポーズ、または「雰囲気（Vibe）」を転写することができます。

## 構図・ポーズの制御

```python
from novelai.types import ControlNet, ControlNetImage, GenerateImageParams

controlnet_image = ControlNetImage(image="pose_reference.png", strength=0.6)
controlnet = ControlNet(images=[controlnet_image])

params = GenerateImageParams(
    prompt="1girl, dancing, ballerina",
    model="nai-diffusion-4-5-full",
    controlnet=controlnet,
)
```
