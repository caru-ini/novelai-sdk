# ControlNet (Vibe Transfer)

ControlNet (including Vibe Transfer and Palette Transfer in NovelAI) allows you to transfer composition, pose, or "vibe" from a reference image.

## Composition/Pose Control

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
