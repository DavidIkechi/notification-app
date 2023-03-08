# Schemas
from pydantic import BaseModel

class ClientSchema(BaseModel):
    slug: str
    client_key: str