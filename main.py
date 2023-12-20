from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "Hola mundo"

@app.get("/url")
async def url():
    return { "autor": "David" }