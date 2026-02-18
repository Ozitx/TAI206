#python app.py // correr servidor de flask
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000/v1/usuarios"

@app.route("/")
def index():
    response = requests.get(API_URL)
    data = response.json()
    usuarios = data["data"] if "data" in data else []
    return render_template("index.html", usuarios=usuarios)

@app.route("/agregar", methods=["POST"])
def agregar():
    id = int(request.form["id"])
    nombre = request.form["nombre"]
    edad = int(request.form["edad"])
    
    usuario = {
        "id" : id,
        "nombre" : nombre,
        "edad" : edad
    } 
    requests.post(API_URL, json=usuario)
    return redirect("/")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)