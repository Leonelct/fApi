from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "entorno": "Virtual Python"}

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola {nombre}, tu API funciona perfectamente"}