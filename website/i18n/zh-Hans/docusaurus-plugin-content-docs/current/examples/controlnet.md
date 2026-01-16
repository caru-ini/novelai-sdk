# ControlNet (Vibe Transfer)

ControlNet (包括 NovelAI 中的 Vibe Transfer 和 Palette Transfer) 允许您从参考图像中转移构图、姿势或“氛围”。

## 构图/姿势控制

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
