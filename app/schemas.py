from pydantic import BaseModel

# BaseModel is  a class used in FastAPI for automatic data
# validation, type safety, cleaner code and auto-generated docs

class PostCreate(BaseModel):
    # request body data should have the following info:
    title: str
    content: str