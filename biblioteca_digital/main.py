from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from models import Libro, LibroCreate, Prestamo, PrestamoCreate
import uuid

app = FastAPI(title="API Biblioteca Digital", version="1.0.0")

# Base de datos en memoria (diccionarios)
libros = {}
prestamos = {}


#ENDPOINT 1: Registrar un libro
@app.post("/libros", response_model=Libro, status_code=201)
def registrar_libro(libro_data: LibroCreate):
    for lib in libros.values():
        if lib["nombre"].lower() == libro_data.nombre.lower():
            raise HTTPException(status_code=400, detail="Ya existe un libro con ese nombre")

    libro_id = str(uuid.uuid4())
    nuevo_libro = Libro(id=libro_id, estado="disponible", **libro_data.dict())
    libros[libro_id] = nuevo_libro.dict()
    return nuevo_libro


#ENDPOINT 2: Listar todos los libros
@app.get("/libros", response_model=List[Libro])
def listar_libros():
    return list(libros.values())


#ENDPOINT 3: Buscar libro por nombre
@app.get("/libros/buscar", response_model=List[Libro])
def buscar_libro(nombre: str):
    if not nombre.strip():
        raise HTTPException(status_code=400, detail="El parámetro nombre no puede estar vacío")
    resultados = [lib for lib in libros.values() if nombre.lower() in lib["nombre"].lower()]
    return resultados


#ENDPOINT 4: Registrar préstamo
@app.post("/prestamos", response_model=Prestamo, status_code=201)
def registrar_prestamo(prestamo_data: PrestamoCreate):
    libro = libros.get(prestamo_data.libro_id)
    if not libro:
        raise HTTPException(status_code=400, detail="El libro no existe")
    if libro["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado")

    prestamo_id = str(uuid.uuid4())
    nuevo_prestamo = Prestamo(
        id=prestamo_id,
        fecha_prestamo=date.today(),
        **prestamo_data.dict()
    )
    prestamos[prestamo_id] = nuevo_prestamo.dict()
    libros[prestamo_data.libro_id]["estado"] = "prestado"
    return nuevo_prestamo


#ENDPOINT 5: Marcar libro como devuelto
@app.put("/prestamos/{prestamo_id}/devolver", response_model=Prestamo)
def devolver_libro(prestamo_id: str):
    prestamo = prestamos.get(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=409, detail="El registro de préstamo no existe")
    if prestamo.get("fecha_devolucion"):
        raise HTTPException(status_code=409, detail="Este préstamo ya fue devuelto")

    prestamos[prestamo_id]["fecha_devolucion"] = date.today().isoformat()
    libros[prestamo["libro_id"]]["estado"] = "disponible"
    return prestamos[prestamo_id]


#ENDPOINT 6: Eliminar registro de préstamo
@app.delete("/prestamos/{prestamo_id}")
def eliminar_prestamo(prestamo_id: str):
    prestamo = prestamos.get(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=409, detail="El registro de préstamo no existe")

    if libros.get(prestamo["libro_id"], {}).get("estado") == "prestado":
        libros[prestamo["libro_id"]]["estado"] = "disponible"

    del prestamos[prestamo_id]
    return {"message": f"Préstamo {prestamo_id} eliminado correctamente"}