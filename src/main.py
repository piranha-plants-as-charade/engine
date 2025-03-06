import os
import asyncio

from env import ENV


# TODO: Create generation process.
async def generate(input_path: str) -> str:

    output_path = os.path.join(ENV.OUTPUT_DIR, os.path.basename(input_path))

    await asyncio.sleep(2)
    os.system(f"cp {input_path} {output_path}")

    return output_path
