from fastapi import FastAPI, HTTPException

app = FastAPI()

text_posts = {
    1: {"title": "New Post", "content": "Test post."},
    2: {"title": "Another Post", "content": "This is the second post."},
    3: {"title": "FastAPI Tips", "content": "Tips for using FastAPI effectively."},
    4: {"title": "Python Tricks", "content": "Some neat Python tricks to try."},
    5: {"title": "Hello World", "content": "The classic first program example."},
}

# "@" is a decorator which wraps a func
# For FastAPI it registers the function below it 
# e.g. Stores the function reference, adds it to the routing table and extracts type hints
# After the function, it attaches metadata (path, method, docs, validation)
@app.get("/posts")
def get_all_posts(limit: int=None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)