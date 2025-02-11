from pydantic import BaseModel, ConfigDict, validate_call


strict_validate_call = validate_call(config=ConfigDict(strict=True))


class StrictBaseModel(BaseModel):
    class Config(ConfigDict):
        strict = True
