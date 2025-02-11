from pydantic import Field

from lib.pydantic_addons import StrictBaseModel


class Note(StrictBaseModel):
    pitch: int = Field(...)
    start: int = Field(..., ge=0)
    duration: int = Field(..., gt=0)

    @property
    def end(self) -> int:
        return self.start + self.duration