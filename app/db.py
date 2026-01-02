# to enable Object Relational Mapping (ORM) - 
# allowing user to write in python rather than SQL/noSQL
# SQLAlchemy in this example

from collections.abc import AsyncGenerator # for type hints when working with async database sessions
import uuid # to generate unique identifier
from sqlalchemy import Column, String, Text, DateTime, ForeignKey # define table columns and relationships.
from sqlalchemy.dialects.postgresql import UUID # native UUID type for postgres
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker # talk to the database asynchronously
from sqlalchemy.orm import DeclarativeBase, relationship
# DeclarativeBase is the base class for all models and relationship defines relationships between tables
from datetime import datetime
from fastapi_user.db import SQLAlchemyUserDatabase, SQLAlchemyUserTableUUID
from fastapi import Depends

# want to use sqlite and aiosqlite(async sqlite) locally
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# sqlaclhemy 2.0 will not allow you to use DeclarativeBase directly as its a base-class factory, not the base itself
class Base(DeclarativeBase):
    pass

# predefined SQLAlchemy table for users with UUID primary key, email, hashed password,
# features such as is_active / is_superuser / etc. and it inherits from SQLAlchemy DeclarativeBase
class User(SQLAlchemyUserTableUUID, Base):
    posts = relationship("Post", back_populates="user") # it allows a user to have many posts, as it links a user to a post
    # if we wanted to flip the one to many relationship around i.e. one post to many users,
    # then the foreign key would have to be here instead i.e. foreign key refers to the one attr in the object that will be many

class Post(Base):
    __tablename__ = "posts"

    # if no as_uuid=True, then will return the generated uuid4 value as a string
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # primary_key ensures that every value is unique
    # No collisions as uuid4 has 122 random bits, ID is generated in Python before insert and works perfectly with async FastAPI
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    # for the foreign key, the user_id must match the id in the user table and it cannot be empty
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utc)
    
    user = relationship("User", back_populates="posts")

engine  = create_async_engine(DATABASE_URL) # creates an async db engine, which prepares the connection machinery
async_session_maker = async_sessionmaker(engine, expire_on_commit=False) # creates a factory for AsyncSession objects,
# where expire_on_commit=False means that after commit(), objects keep their values otherwise SQLAlchemy would re-fetch
# data from DB which causses issues for async apps

# note if a DB already exists, but the tables (or some) don't, it will generate the tables
async def create_db_and_tables():
    # opens a db connection, starts a transaction, automatically commits if successful,
    # rolls back if there’s an error and closes the connection
    async with engine.begin() as conn: 
        # the input here inspects all models that inherit from DeclarativeBase, generates SQL CREATE TABLE statements and
        # executes them only if the tables don’t already exist
        await conn.run_sync(Base.metadata.create_all) # note for prod, alembic migrations should be used

# this method will allow us to get a session of the database where we can write and read etc. to it
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)