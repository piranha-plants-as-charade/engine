import os
import uuid
import mimetypes
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
    upload_path = os.path.join(
        ENV.INPUT_DIR, f"{uuid.uuid4()}{ext}"
    )  # UUID is guaranteed to be unique

    # Save file to disk.
    with open(upload_path, "wb") as fout:
        content = await file.read()
        fout.write(content)

    output_path = await main.generate(input_path=upload_path)
    output_mime_type = mimetypes.guess_type(output_path)[0]
    assert output_mime_type in (
        "audio/wav",
        "audio/x-wav",  # audio/wav and audio/x-wav are identical
    )

    return FileResponse(
        path=output_path,
        media_type="audio/wav",
    )
