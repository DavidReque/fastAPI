from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
async def products():
    return ["Producto1", "Producto2", "Producto3",]