from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate
from app.db import Post, create_db_and_tables, create_async_engine
from sqlalchemy.ext.asyncio import  AsyncSession
from contextlib import asynccontextmanager

# FastAPI lifespan handler, where code runs when the app starts, and (optionally) when it shuts down
# As code before yield, runs at startup and code after yield, runs at shutdown
# FastAPI now recommends lifespan instead of @app.on_event("startup") for cleaner async handling and better error control
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# text_posts = {
#     1: {"title": "New Post", "content": "Test post."},
#     2: {"title": "Another Post", "content": "This is the second post."},
#     3: {"title": "FastAPI Tips", "content": "Tips for using FastAPI effectively."},
#     4: {"title": "Python Tricks", "content": "Some neat Python tricks to try."},
#     5: {"title": "Hello World", "content": "The classic first program example."},
# }

# "@" is a decorator which wraps a func
# For FastAPI it registers the function below it 
# e.g. Stores the function reference, adds it to the routing table and extracts type hints
# After the function, it attaches metadata (path, method, docs, validation)
# @app.get("/posts")
# def get_all_posts(limit: int=None):
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts

# include returned or out value for improving docs
# @app.get("/posts/{id}")
# def get_post(id: int) -> PostCreate:
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return text_posts.get(id)

# @app.post("/posts")
# def create_post(post: PostCreate) -> PostCreate:
#     new_post ={"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys()) + 1] = new_post
#     return new_post