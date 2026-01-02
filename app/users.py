import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from app.db import User, get_user_db
from dotenv import load_dotenv
import os

SECRET = os.getenv("SECRET") # wihout one, people could pretend to be any user and forge tokens
# When you generate a token, the server signs it with SECRET and when a client sends a token, the server verifies the signature


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    # FastAPI handles things like verification, password resets (on_after_forgot_password   ) etc. here,
    #  but the user is able to override methods with an example below
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db) # injecting the user_db inside the UserManager Class 


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login") # login endping is the tokenURL

def  get_jwt_strategy():
    return JWTStrategy(secret=os.getenv("SECRET"), lifetime_seconds=3600) # lifetime_seconds is how long the token is valid for

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)

# give the model that will be used, the user manager, and the backend that will be used, which is with the jwt token
fastapi_users =  FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
# when the current active user items is called, it will give the current active user by going and checking the users jwt token
current_active_user = fastapi_users.current_user(active=True)