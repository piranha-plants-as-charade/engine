import mimetypes


def db_to_strength(db: float) -> float:
    return 10 ** (db / 20)


def is_wav_media_type(path: str) -> bool:
    media_type = mimetypes.guess_type(path)[0]
    return media_type in (
        "audio/wav",
        "audio/x-wav",  # audio/wav and audio/x-wav are identical
    )
