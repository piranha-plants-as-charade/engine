import os
import asyncio

EXPORT_DIR = "../outputs"


# TODO: Create generation process.
async def generate(input_path: str) -> str:

    os.makedirs(EXPORT_DIR, exist_ok=True)
    export_path = os.path.join(EXPORT_DIR, os.path.basename(input_path))

    await asyncio.sleep(2)
    os.system(f"cp {input_path} {export_path}")

    return export_path
