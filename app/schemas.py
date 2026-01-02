from pydantic import BaseModel
from fastapi_users import schemas
import uuid

# BaseModel is  a class used in FastAPI for automatic data
# validation, type safety, cleaner code and auto-generated docs

class PostCreate(BaseModel):
    # request body data should have the following info:
    title: str
    content: str

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass