from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=["Varios"])

#Endpoints
@router.get("/")
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@router.get("/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST"}

#EndPoint con delay simulado
@router.get("/v1/calificaciones")
async def califiaciones():
    await asyncio.sleep(5)
    return {"mensaje": "tu calificacion en TAI es 10"}

#Endpoint con parametros obligatorios
@router.get("/v1/parametroo/{id}")
async def consultausuarios(id:int):
    await asyncio.sleep(5)
    return {"Usuario encontrado":id}

#Endpoint con parámetros opcionales
@router.get("/v1/parametroOP/")
async def consultaop(id:Optional[int]=None):
    await asyncio.sleep(5)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id:
                return {"Usuario encontrado":id, "usuario":usuario}
        return {"Mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporciono id"}
