from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def products():
    return ["Producto1", "Producto2", "Producto3",]