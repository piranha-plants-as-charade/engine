import os
import uuid
import dataclasses
from dataclasses import dataclass
from typing import Annotated
from fastapi import FastAPI, UploadFile, File, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse, JSONResponse

from common.util import is_wav_media_type

import main
from logger import LOGGER
from env import ENV


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ENV.FE_BASE_URL],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization"],
)


@dataclass
class HealthResponse:
    status: str = "healthy"

    def as_dict(self):
        return dataclasses.asdict(self)


def authorize(token: str) -> bool:
    return token == "Bearer " + ENV.BE_AUTH_TOKEN


def generate_unique_file_name(file: UploadFile) -> str:
    name = str(uuid.uuid4())  # UUID is guaranteed to be unique
    ext = ""
    if file.filename is not None:
        ext = os.path.splitext(file.filename)[1]
    return name + ext


@app.get("/healthz", responses={status.HTTP_200_OK: {"model": HealthResponse}})
def healthz():
    return JSONResponse(content=HealthResponse().as_dict())


@app.post(
    "/generate",
    response_class=FileResponse,
    responses={
        status.HTTP_200_OK: {
            "content": {"audio/wav": {}},
            "description": "Returns the generated arrangement in the style of _Piranha Plants on Parade_.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Requires the proper bearer token."
        },
    },
)
async def generate(
    authorization: Annotated[
        str,
        Header(
            description="A bearer token used for authorization.",
        ),
    ],
    file: Annotated[
        UploadFile,
        File(
            description="An audio file containing a melody to arrange in the style of _Piranha Plants on Parade_."
        ),
    ],
) -> Response:
    LOGGER.info("Requested /generate.")

    if not authorize(authorization):
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # TODO: validate file.

    upload_path = os.path.join(ENV.INPUT_DIR, generate_unique_file_name(file))
    upload_id = os.path.splitext(os.path.basename(upload_path))[0]

    LOGGER.info(f"Handling input with ID {upload_id}")

    # Save file to disk.
    with open(upload_path, "wb") as fout:
        content = await file.read()
        fout.write(content)

    output_path = await main.generate(input_path=upload_path)
    assert is_wav_media_type(output_path)

    return FileResponse(
        status_code=status.HTTP_200_OK,
        path=output_path,
        media_type="audio/wav",
    )
