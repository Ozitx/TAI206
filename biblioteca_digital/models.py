from pydantic import BaseModel, Field, EmailStr, filed_validator
from typing import Optional
from datetime import date

ANIO_ACTUAL = date.today().year


class LibroCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str = Field(..., min_length=2, max_length=100)
    anio_publicacion: int
    paginas: int

    @filed_validator("anio_publicacion")
    def validar_anio(cls, v):
        if v <= 1450:
            raise ValueError("El año debe ser mayor a 1450")
        if v > ANIO_ACTUAL:
            raise ValueError(f"El año no puede ser mayor a {ANIO_ACTUAL}")
        return v

    @filed_validator("paginas")
    def validar_paginas(cls, v):
        if v < 1:
            raise ValueError("Las páginas deben ser mayor a 1")
        return v


class Libro(LibroCreate):
    id: str
    estado: str = "disponible"

    @filed_validator("estado")
    def validar_estado(cls, v):
        if v not in ["disponible", "prestado"]:
            raise ValueError("Estado debe ser 'disponible' o 'prestado'")
        return v


class PrestamoCreate(BaseModel):
    libro_id: str
    nombre_usuario: str = Field(..., min_length=2, max_length=100)
    correo_usuario: EmailStr


class Prestamo(PrestamoCreate):
    id: str
    fecha_prestamo: date
    fecha_devolucion: Optional[date] = None