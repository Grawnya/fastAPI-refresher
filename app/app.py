from fastapi import FastAPI

app = FastAPI()

text_posts = {}

# "@" is a decorator which wraps a func
# For FastAPI it registers the function below it 
# e.g. Stores the function reference, adds it to the routing table and extracts type hints
# After the function, it attaches metadata (path, method, docs, validation)
@app.get("/posts")
def get_all_posts():
    return text_posts