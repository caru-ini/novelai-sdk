# Streaming Generation

Image generation can take seconds to tens of seconds.
SSE (Server-Sent Events) streaming allows you to receive the generation process in real-time.
This provides feedback to the user that something is happening, reducing perceived latency.

```python
from novelai.types import GenerateImageStreamParams
from base64 import b64decode

# Client initialization (omitted)

params = GenerateImageStreamParams(
    prompt="masterpiece, best quality, scenery, detailed",
    model="nai-diffusion-4-5-full",
    stream="sse", # Enable stream mode
    steps=28,
)

# Use generate_stream method
for chunk in client.image.generate_stream(params):
    if chunk.image:
        image_data = b64decode(chunk.image)
        print(f"Received chunk: {len(image_data)} bytes")
        # You can send data to frontend or update preview here
```
