import typing
import pydantic

from errors import BadRequest


class PostAds(pydantic.BaseModel):
    title: str
    description: str
    owner: str


class PatchAds(pydantic.BaseModel):
    title: typing.Optional[str]
    description: typing.Optional[str]


def validate(template, data: dict):
    try:
        return template(**data).dict()
    except pydantic.ValidationError as error:
        raise BadRequest(error.errors())