from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$04$S78QVDqWsLEkafpe1Rj4NOSh3/Fw9UwmSIt1owdUlRRRfhnQRxeN"
    },
    "Juan": {
        "username": "Juan",
        "full_name": "J",
        "email": "juan@gmail.com",
        "disabled": True,
        "password": "$2a$04$dGOpvQWYZfJaUY1UjjdPm.SWBCWrIp/PPFVoiXG27FMrT62nz8f02"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db: 
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto"
        )
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="la contraseña no es correcta"
        )
    
    return {"access_token": user.username, "token_type": "bearer"}
