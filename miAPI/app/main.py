#cd miAPI
#uvicorn main:app --reload
#importaciones

from fastapi import FastAPI 
import asyncio
from typing import Optional

#Inicialización
app= FastAPI( title='My first API', description='Cynthia Resendiz Ramos', version='1.0')

#diccionario
usuarios=[
    {"id":1,"nombre":"yancarlos","edad":"18"},
    {"id":2,"nombre":"alexis","edad":"15"},
    {"id":3,"nombre":"gustavo","edad":"18"},
]

#Endpoints
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST"}

#EndPoint con delay simulado
@app.get("/v1/calificaciones", tags=['Asincronia'])
async def califiaciones():
    await asyncio.sleep(5)
    return {"mensaje": "tu calificacion en TAI es 10"}

#Endpoint con parametros obligatorios
@app.get("/v1/usuarios{id}", tags=['Obligatorio'])
async def consultausuarios(id:int):
    await asyncio.sleep(5)
    return {"Usuario encontrado":id}

#Endpoint con parámetros opcionales
@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaop(id:Optional[int]=None):
    await asyncio.sleep(5)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id:
                return {"Usuario encontrado":id, "usuario":usuario}
        return {"Mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporciono id"}