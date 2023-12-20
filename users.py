from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    surname: str
    lastname: str
    age: int

user_list = [
        User(
            name="David",
            surname="Davv",
            lastname="Requeno",
            age=19
        ),
        User(
            name="Juan",
            surname="j",
            lastname="G",
            age=30
        ),
    ]

@app.get("/usersjson")
async def usersjson():
    return [{"name": "David", "surname": "Davidd"}]

@app.get("/users")
async def users():
    return user_list
            