from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import  AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

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

#note that FastAPI is async by default
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session) # dependency injection to get an async DB session before func can run
):
    post = Post(
        caption=caption,
        url="dummy url",
        file_type="photo",
        file_name="dummy name"
    )
    session.add(post) # acts as if staging the post to be saved
    await session.commit() # commits the new post to be saved
    await session.refresh(post) # gets the post but with the extra id and created at details generated when committing to DB
    return post

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc())) #can do .filter_by for more filtering etc.,
    # result var is of type cursor object
    posts = [row[0] for row in result.all()] # step through all results and convert to list

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": posts_data}