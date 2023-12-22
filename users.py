from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    lastname: str
    age: int

user_list = [
        User(
            id=1,
            name="David",
            surname="Davv",
            lastname="Requeno",
            age=19
        ),
        User(
            id=2,
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

#Path
@app.get("/user/{id}")
async def user(id: int):
        return search_user(id)
            
#Query
@app.get("/userquery/")
async def user(id: int):
    return search_user(id)
        
def search_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except: 
        return {"error": "No se ha encontrado el usuario"}