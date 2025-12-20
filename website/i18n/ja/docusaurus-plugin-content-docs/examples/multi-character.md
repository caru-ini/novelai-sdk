# マルチキャラクターポジショニング

複数のキャラクターを生成する際、それぞれのキャラクターの特徴（髪色や目の色、服装など）が混ざってしまうことがあります。
マルチキャラクターポジショニング機能を使うと、各キャラクターに別々のプロンプトと位置を指定でき、混ざりを防ぐことができます。

```python
from novelai.types import Character, GenerateImageParams

characters = [
    Character(
        prompt="1girl, red hair, blue eyes, school uniform",
        enabled=True,
        position=(0.2, 0.5), # 左側 (X: 0.2, Y: 0.5)
    ),
    Character(
        prompt="1boy, black hair, green eyes, casual clothes",
        enabled=True,
        position=(0.8, 0.5), # 右側 (X: 0.8, Y: 0.5)
    ),
]

params = GenerateImageParams(
    # 全体のプロンプトも指定可能ですが、キャラクターの詳細は上記で指定します
    prompt="two people standing together, holding hands, best quality",
    model="nai-diffusion-4-5-full",
    characters=characters,
)
```
