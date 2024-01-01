from fastapi import FastAPI, HTTPException
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
async def get_user_by_id(id: int):
        return search_user(id)
            
#Query
@app.get("/userquery/")
async def get_user_by_query(id: int):
    return search_user(id)

#post
@app.post("/user/", status_code=201)
async def create_user(user: User):
     if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
     else:
        user_list.append(user)
        return user

#put
@app.put("/user/")
async def update_user(user: User):

    found = False

    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user
    
#delete
@app.delete("/user/{id}")
async def delete_user_by_id(id: int):

    found = False

    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            found = True

    if not found:
        return {"error": "No se ha eliminado el usuario"}
    else: 
        return "El usuario se elimino"

def search_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except: 
        return {"error": "No se ha encontrado el usuario"}
