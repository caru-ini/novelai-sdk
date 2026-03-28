---
sidebar_position: 4
title: Anlas計算
---

# Anlas計算

このページでは、SDK が現在使っている Anlas 見積もりロジックをまとめています。

これは現在の NovelAI WebUI と公式ドキュメントをもとにした best-effort な
推定値です。プレビュー用途には使えますが、課金額を 100% 保証するものでは
ありません。

## 含まれるもの

- 基本の画像生成コスト
- Opus の軽量割引
- img2img / inpaint の strength 補正
- high-level API における未キャッシュ Vibe の encoding surcharge
- 5件目以降の Vibe surcharge
- Character Reference surcharge

## 簡単な例

```python
from novelai.types import GenerateImageParams

params = GenerateImageParams(
    prompt="1girl, night city",
    model="nai-diffusion-4-5-full",
    size=(1024, 1024),
    steps=28,
)

estimate = params.calculate_anlas(is_opus=True)
print(estimate.total_anlas)
print(estimate.base_anlas)
```

## 注意点

- `str(estimate)` は合計 Anlas を返します
- `int(estimate)` も同じ合計値を返します
- low-level の `calculate_anlas(model, ImageParameters)` では raw cache state が
  ないため、未キャッシュ Vibe の encoding cost は推定できません

実装時に使った逆解析メモの詳細は、リポジトリ内の `docs/for-ai/anlas-calculation.md`
を参照してください。
