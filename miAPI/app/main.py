#cd miAPI
#uvicorn main:app --reload
#importaciones

from fastapi import FastAPI
from app.routers import usuarios, misc

#Inicialización / instancia del servidor
app= FastAPI( title='My first API', description='Cynthia Resendiz Ramos', version='1.0')

app.include_router(usuarios.router)
app.include_router(misc.router)