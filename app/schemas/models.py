from pydantic import BaseModel


class UserSchemaResponse(BaseModel):
    id: int
    name: str


class UserSchema(BaseModel):
    name: str
