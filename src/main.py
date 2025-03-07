import os
import asyncio

from env import ENV


# TODO: Create generation process.
async def generate(input_path: str) -> str:

    name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(ENV.OUTPUT_DIR, f"{name}.wav")

    await asyncio.sleep(2)
    os.system(f"ffmpeg -i {input_path} {output_path}")

    return output_path
