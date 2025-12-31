# Application Programming Interface (API) project quick setup
- `python -m venv venv` - to create a venv in correct environment
- `venv\Scripts\Activate` - activate that environment in windows (different for linux/docker)

Get the below from the `requirements.txt`:
- `pip install uvicorn` - python server which allows us to serve fastapi app
- `pip install python-dotenv` - for dealing with enviornmental vars
- `pip install fastapi-users[sqlalchemy]` - to deal with user authnetication adn authorisation through a self made profile (non MS for Entra ID)
- `pip install imagekitio` - to deal with images in app, but normally with S3 bucket
- Create env vars for imagekit and get the private and public key along with the URL from the "Developer Options" page.