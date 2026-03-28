---
sidebar_position: 4
title: Anlas 计算
---

# Anlas 计算

本页总结了 SDK 当前使用的 Anlas 估算逻辑。

它基于当前 NovelAI WebUI 与官方文档整理而成，属于 best-effort 估算，
适合用于预览，但不能视为 100% 准确的计费真值来源。

## 包含的内容

- 基础图片生成费用
- Opus 轻量折扣
- img2img / inpaint 的 strength 修正
- high-level API 中未缓存 Vibe 的 encoding surcharge
- 第五个及之后的 Vibe surcharge
- Character Reference surcharge

## 简单示例

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

## 注意事项

- `str(estimate)` 会返回总 Anlas 值
- `int(estimate)` 也会返回同一个总值
- low-level 的 `calculate_anlas(model, ImageParameters)` 无法判断未缓存
  Vibe 的 encoding cost，因为那里已经没有原始 cache state

如果你想查看实现时使用的逆向分析说明，请参考仓库中的
`docs/for-ai/anlas-calculation.md`。
