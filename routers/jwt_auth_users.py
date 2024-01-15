from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "228ec9c36cd92b8d4b7cd5e81456b5d994fd1d7251442ce7f03a3138f54a8052"

router = APIRouter()

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

def search_user_db(username: str = Depends(oauth2)):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    return User(**users_db[username])
    
async def auth_user(token: str):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalidas", 
            headers={"WWW-Authenticate", "Bearer"}
        ) 

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
               raise exception
    
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo", 
        )
    
    return user

@router.post("/login")
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
    
    encoded_jwt = jwt.encode(access_token, SECRET, algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer", "info": access_token}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user