from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

#Inicialización
app= FastAPI( title='Sistema de citas Medicas', description='Cynthia Resendiz Ramos', version='1.0')

#Configuración de OAuth2
SECRET_KEY = "clave-secreta-TAI206"
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

#validaciones pydantic
class UsuarioBase(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(..., min_length=5, max_length=50, description="Nombre del usuario")
    
class cita(BaseModel):
    fecha: 
    motivo: str = Field(..., min_length= 5, max_digits=100, description="Motivo de la consulta")
    confirmacion: bool = Field(..., False, description="Confirmacion de cita")
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None


#Seguridad con JWT
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

#pacientes
usuarios=[
    {"id":1,"nombre":"cynthia","edad":"20"},
    {"id":2,"nombre":"Eduardo","edad":"20"},
    {"id":3,"nombre":"Jorge","edad":"20"},
    {"id":4,"nombre":"Daniel","edad":"20"},
    {"id":5,"nombre":"Sara","edad":"20"},
]

#Endpoint del login que genera el token JWT
@app.post("/token", response_model=Token, tags=["Autenticación"])
async def login(from_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(from_data.username, from_data.password)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crear_token(
        data = {"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", tags=['Inicio'])
async def inicio():
    return {"mensaje": "funciona"}

#Endpoints protegidos con JWT
@app.get("/")