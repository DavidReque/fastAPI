from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

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
        "password": "$2a$12$UzUS3ePnaby9rUbkZ3omIelV00JOhVW35ZKV1cXVAayWMcP/wVOhK"
    },
    "Juan": {
        "username": "Juan",
        "full_name": "J",
        "email": "juan@gmail.com",
        "disabled": True,
        "password": "$2a$12$GaZ4t5p5QArittZeLq6bvO2jcJC23P3.gs36AmsRjXqJAbButyETK"
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

    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    encoded_jwt = jwt.encode(access_token, "secret", algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}

