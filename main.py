import uvicorn

if __name__ == "__main__":
    # python server, run app folder, app.py file and then the :app FastAPI,
    # host is the domain, which "0.0.0.0" means any available domain in this case localhost as run locally
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)