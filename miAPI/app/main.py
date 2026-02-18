#cd miAPI
#uvicorn main:app --reload
#importaciones

from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

#Inicialización
app= FastAPI( title='My first API', description='Cynthia Resendiz Ramos', version='1.0')

#diccionario
usuarios=[
    {"id":1,"nombre":"yancarlos","edad":18},
    {"id":2,"nombre":"alexis","edad":15},
    {"id":3,"nombre":"gustavo","edad":19},
    {"id":4,"nombre":"edgar","edad":19},
    {"id":5,"nombre":"alan","edad":21},
    {"id":6,"nombre":"jorge","edad":19},

]

#Modelo de validación pydantic
class UsuarioBase(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad: int = Field(..., ge=0, le=120, description="Edad valida entre 0 y 120")


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
@app.get("/v1/parametroo/{id}", tags=['Parametro Obligatorio'])
async def consultausuarios(id:int):
    await asyncio.sleep(5)
    return {"Usuario encontrado":id}

#Endpoint con parámetros opcionales
@app.get("/v1/parametroOP/", tags=['Parametro Opcional'])
async def consultaop(id:Optional[int]=None):
    await asyncio.sleep(5)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id:
                return {"Usuario encontrado":id, "usuario":usuario}
        return {"Mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporciono id"}
    
@app.get ("/v1/usuarios/", tags=['CRUD Usuarios'])
async def consultausuario():
    return{
        "status": "200",
        "total": len(usuarios),
        "data":usuarios
    }
    
@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
async def agregar_usuarios(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuarios.append(usuario)
    return{
        "Mensaje": "Usuario agregado",
        "datos":usuario,
        "status":"200"
    }
        
@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuarios(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return{
            "Mensaje": "Usuario actualizado",
            "datos": usuario_actualizado
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuarios(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return{
                "mensaje": "Usuario eliminado",
                "datos": usr
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")