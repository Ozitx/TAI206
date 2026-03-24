
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter

#**************************
#Importación de archivos
#**************************
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(prefix="/v1/usuarios", tags=["CRUD HTTP"])

@router.get ("/")
async def consultausuario(db:Session = Depends(get_db)):
    
    consultausuarios= db.query(usuarioDB).all()
    return{
        "status": "200",
        "total": len(usuarios),
        "usuarios":consultausuarios
    }
    
@router.post("/", status_code=status.HTTP_200_OK)
async def agregar_usuarios(usuarioP:UsuarioBase, db:Session= Depends(get_db)):
    
    nuevoUsuario=usuarioDB(nombre= usuarioP.nombre,edad= usuarioP.edad)
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)

    return{
        "Mensaje": "Usuario agregado",
        "datos":nuevoUsuario,
        "status":"200"
    }
        
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuarios(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return{
            "Mensaje": "Usuario actualizado",
            "datos": usuario_actualizado
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuarios(id: int, usuarioAuth: str= Depends(verificar_Peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return{
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "datos": usr
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")