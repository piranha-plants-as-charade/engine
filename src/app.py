import os
import tempfile
import dataclasses
from typing import Dict, Any
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

import main

UPLOAD_DIR = "../inputs"


app = FastAPI()


@dataclasses.dataclass
class UploadAudioResponse:
    upload_path: str

    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@app.post("/generate")
async def generate(file: UploadFile) -> FileResponse:

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file to disk.
    upload_file = tempfile.NamedTemporaryFile(
        dir=UPLOAD_DIR,
        suffix=".wav",
        delete=False,
    )
    content = await file.read()
    upload_file.write(content)

    export_path = await main.generate(input_path=upload_file.name)

    upload_file.close()
    os.remove(upload_file.name)

    return FileResponse(
        path=export_path,
        media_type="audio/wav",
    )
