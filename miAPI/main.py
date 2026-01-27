#importaciones
from fastapi import FastAPI

#Inicialización
app= FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST"}