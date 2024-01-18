from fastapi import APIRouter, HTTPException
from  db.models.user import User
from db.client import db_client

router = APIRouter(prefix="/userdb", 
                   tags=["userdb"],
                   responses={404: {"message": "No encontrado"}})

user_list = []

@router.get("/")
async def users():
    return user_list

#Path
@router.get("/{id}")
async def get_user_by_id(id: int):
        return search_user(id)
            
#Query
@router.get("/usersdbquery/")
async def get_user_by_query(id: int):
    return search_user(id)

#post
@router.post("/", response_model=User, status_code=201)
async def create_user(user: User):
     #if type(search_user(user.id)) == User:
        #raise HTTPException(status_code=204, detail="El usuario ya existe")
     #else:
        
    user_dict = dict(user)   

    db_client.local.users.insert_one(user_dict)

    return user

#put
@router.put("/")
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
@router.delete("/{id}")
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
