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




@app.get("/encrS/{text}")
def verificar_password(nombre:str, passwordI:str) -> bool:
    eejj = {nombre:"Leonel", password:"$2b$12$MS5I.mIRh6yHo7K/WbFr1u.xH.ScCHNHbTbfqhfR6pZkTM/W6nyHu"}
    # Convertimos ambos a bytes para la comparación
    pIngresada_bytes = passwordI.encode('utf-8')
    password_bytes = password.encode('utf-8')
    
    # bcrypt.checkpw detecta automáticamente el salt dentro del hash
    return bcrypt.checkpw(pIngresada_bytes, password_bytes)