#cd miAPI
#uvicorn main:app --reload
#importaciones

from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

#Inicialización
app= FastAPI( title='My first API', description='Cynthia Resendiz Ramos', version='2.0')

#======================================
# Configuración OAuth2 + JWT
#=====================================
SECRET_KEY = "clave-secreta-super-segura-TAI206"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#dashear contraseñas con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#indica a la fastAPI donde obtener el token
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="token")

#=========================
# Base de usuario similada
#=========================
fake_users_bd = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("123456789")
    }
}

#Modelo de validación pydantic
class UsuarioBase(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad: int = Field(..., ge=0, le=120, description="Edad valida entre 0 y 120")
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None
    
#**************************************
#Seguridad con JWT
#**************************************
    
def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
    
def autenticar_usuario(username: str, password: str):
    user = fake_users_bd.get(username)
    if not user:
        return False
    if not verificar_password(password, user["hashed_password"]):
        return False
    return user

def crear_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt. encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token : str = Depends(oauth2_scheme)) -> str:
    credentrials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentrials_exception
        return username
    except JWTError:
        raise credentrials_exception

#diccionario
usuarios=[
    {"id":1,"nombre":"yancarlos","edad":18},
    {"id":2,"nombre":"alexis","edad":15},
    {"id":3,"nombre":"gustavo","edad":19},
    {"id":4,"nombre":"edgar","edad":19},
    {"id":5,"nombre":"alan","edad":21},
    {"id":6,"nombre":"jorge","edad":19},

]

#===========================================
#Endpoint del login que genera el token JWT
#===========================================
@app.post("/token", response_model=Token, tags=["Autenticación"])
async def login(from_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(from_data.username, from_data.password)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #access_token = crear_token(
        #data = {"sub": user["username"]},
        #expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #)
    #return {"access_token": access_token, "token_type": "bearer"}

#====================================
#Endpoints publicos (sin protección)
#====================================
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

#=================================
#Endpoints protegidos con JWT
#=================================
@app.put("/v1/usuarios/{id}", tags=["CRUD Usuarios"])
async def actualizar_usuario(
    id: int,
    usuario_actualizado: dict,
    current_user: str = Depends(verificar_token)
):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return{
                "Mensaje": f"Usuario actualizado por {current_user}",
                "datos": usuario_actualizado
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuarios(
    id: int,
    current_user: str = Depends(verificar_token)
    ):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return{
                "mensaje": f"Usuario eliminado por {current_user}",
                "datos": usr
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")