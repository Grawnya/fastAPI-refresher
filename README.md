# General Notes Which Act as a Refresher
## Application Programming Interface (API) Project Quick Setup
- `python -m venv venv` - to create a venv in correct environment
- `venv\Scripts\Activate` - activate that environment in windows (different for linux/docker)
- `.\venv\Scripts\python.exe` to check the python used and ensure the interpreter matches. This can be done in the control panel with "Python: Select Interpreter".

Get the below from the `requirements.txt`:
- `pip install uvicorn` - python server which allows us to serve fastapi app
- `pip install python-dotenv` - for dealing with enviornmental vars
- `pip install fastapi-users[sqlalchemy]` - to deal with user authnetication adn authorisation through a self made profile (non MS for Entra ID)
- `pip install imagekitio` - to deal with images in app, but normally with S3 bucket
- Create env vars for imagekit and get the private and public key along with the URL from the "Developer Options" page.

## Notes for Creating API
- JavaScript Object Notation (JSON)/python dicts or pydantic objects are the only things your methods should return
- Make sure in right folder if running `python main.py`, which calls on `app.py`
- Can add the expected type of a parameter input in a function e.g.:
```
@app.get("/posts/{id}")
def get_post(id: int):
```