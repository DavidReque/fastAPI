from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "David": {
        "username": "David",
        "full_name": "Requeno",
        "email": "dr@gmail.com",
        "disabled": False,
        "password": "david123"
    },
    "Juan": {
        "username": "Juan",
        "full_name": "J",
        "email": "juan@gmail.com",
        "disabled": True,
        "password": "juan123"
    },
}

def search_user(username: str):
    if username in users_db:
        return UserDB(users_db[username])