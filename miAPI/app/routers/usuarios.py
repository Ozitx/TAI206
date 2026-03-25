
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

#____________________GET TODOS___________________________ 
@router.get ("/")
async def consultausuario(db:Session = Depends(get_db)):
    
    consultausuarios= db.query(usuarioDB).all()
    return{
        "status": "200",
        "total": len(usuarios),
        "usuarios":consultausuarios
    }
    
#_____________________GET POR ID__________________________
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def consulta_usuario_id(id: int, db: Session=Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {id } no encontrado"
        )
    return {
        "status": "200",
        "usuario": usuario
    }
    
#_____________________________POST________________________________________
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuarioP:UsuarioBase, db:Session= Depends(get_db)):
    
    nuevoUsuario=usuarioDB(nombre= usuarioP.nombre,edad= usuarioP.edad)
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)

    return{
        "Mensaje": "Usuario agregado",
        "datos":nuevoUsuario,
        "status":"201"
    }
       
#_____________________________________PUT___________________________________________ 
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuario_actualizado: UsuarioBase, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {id} no encontrado"
        )
    usuario.nombre = usuario_actualizado.nombre
    usuario.edad = usuario_actualizado.edad
    db.commit()
    db.refresh(usuario)
    return{
        "Mensaje": "Usuario actualizado",
        "datos": usuario,
        "status": "200"
    }

#__________________________PATCH________________________________________
@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario_dos(id: int, campos: dict, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {id} no encontrado"
        )
    campos_permitidos = {"nombre", "edad"}
    for campo, valor in campos_items():
        if campo not in campos_permitidos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Campo '{campo}' no permitido"
            )
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return{
        "Mensaje": "Usuario actualizado con PATCH",
        "datos": usuario,
        "status": "200"
    }
    
#__________________________DELETE________________________________________
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuarios(id: int, db: Session = Depends(get_db), usuarioAuth: str = Depends(verificar_Peticion)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {id} no encontrado"
        )
    db.delete(usuario)
    db.commit()
    return{
        "Mensaje": f"Usuario eliminado por {usuarioAuth}",
        "datos": {"id": usuario.id, "nombre": usuario.nombre, "edad": usuario.edad},
        "status": "200"
    }