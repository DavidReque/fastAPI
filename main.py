from fastapi import FastAPI
from routers import products

app = FastAPI()

#Routers
app.include_router(products.router)

@app.get("/")
async def root():
    return "Hola mundo"

@app.get("/url")
async def url():
    return { "autor": "David" }