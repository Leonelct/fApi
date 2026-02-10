from fastapi import FastAPI
import bcrypt
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "entorno": "Virtual Python"}

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola {nombre}, tu API funciona perfectamente"}


@app.get("/encr/{text}")
def generar_hash_password(password_plana: str) -> str:
    """
    Transforma la contraseña de texto plano en un hash seguro.
    Se debe usar al momento de REGISTRAR un usuario.
    """
    # Convertimos la contraseña a bytes
    password_bytes = password_plana.encode('utf-8')
    
    # Generamos el salt y el hash
    salt = bcrypt.gensalt()
    hash_resultado = bcrypt.hashpw(password_bytes, salt)
    
    # Retornamos como string para guardarlo fácilmente en la DB (columna password_hash)
    return hash_resultado.decode('utf-8')