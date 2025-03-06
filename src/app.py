import os
import tempfile
import dataclasses
from typing import Dict, Any
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import main
from env import ENV


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ENV.FE_BASE_URL],
)


@dataclasses.dataclass
class UploadAudioResponse:
    upload_path: str

    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@app.post("/generate")
async def generate(file: UploadFile) -> FileResponse:
    assert file.filename is not None
    assert file.content_type is not None

    ext = os.path.splitext(file.filename)[1]

    # Save file to disk.
    upload_file = tempfile.NamedTemporaryFile(
        dir=ENV.INPUT_DIR,
        suffix=ext,
        delete=False,
    )
    content = await file.read()
    upload_file.write(content)

    output_path = await main.generate(input_path=upload_file.name)

    upload_file.close()

    return FileResponse(
        path=output_path,
        media_type=file.content_type,  # TODO: make this audio/wav
    )
