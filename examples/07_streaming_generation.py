"""Streaming generation example

This example shows how to use streaming to receive image data progressively.
This is useful for showing generation progress in real-time applications.
"""

from base64 import b64decode
from pathlib import Path

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import GenerateImageStreamParams

load_dotenv()

client = NovelAI()

prompt = "1girl, standing, very aesthetic, masterpiece"

print("Starting streaming generation...")
total_bytes = 0

params = GenerateImageStreamParams(
    prompt=prompt,
    model="nai-diffusion-4-5-full",
    size=(832, 1216),
    steps=23,
    scale=5.0,
    sampler="k_euler_ancestral",
    seed=1234567890,
    stream="sse",
)

output_path = Path("output") / "streaming_results"
output_path.mkdir(exist_ok=True)


# chunk is progress of the generation (1 image at a time, chunk is a bytes object)
for chunk in client.image.generate_stream(params):
    decoded_image = b64decode(chunk.image.encode("utf-8"))
    total_bytes += len(decoded_image)
    chunk_path = output_path / f"chunk_{total_bytes}.png"
    chunk_path.write_bytes(decoded_image)
    print(f"Received chunk: {len(decoded_image)} bytes (total: {total_bytes} bytes)")


print(f"\nStreaming complete! Received {total_bytes} bytes total")
print(f"Saved to: {output_path}")
