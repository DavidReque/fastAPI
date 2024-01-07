from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db: 
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto"
        )
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="la contraseña no es correcta"
        )
    
    return {"access_token": user.username, "token_type": "bearer"}