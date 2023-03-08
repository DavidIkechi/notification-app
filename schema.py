# Schemas
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class config:
        orm_mode = True

class ClientSchema(BaseModel):
    slug: str
    client_key: str    