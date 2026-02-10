from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Importación necesaria para CORS
from pydantic import BaseModel
import bcrypt

app = FastAPI()

# --- CONFIGURACIÓN DE CORS ---
# Esto permite que tu React (localhost:5173) se comunique con Koyeb
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"], # En producción cambia "*" por tu dominio de frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS ---
class LoginRequest(BaseModel):
    nombre: str
    passwordI: str

# --- RUTAS ---

@app.get("/")
def home():
    return {"status": "Online", "entorno": "Virtual Python"}

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola {nombre}, tu API funciona perfectamente"}

@app.get("/encr/{password_plana}") # Corregido el parámetro para que coincida
def generar_hash_password(password_plana: str):
    """Genera un hash para registrar usuarios."""
    password_bytes = password_plana.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_resultado = bcrypt.hashpw(password_bytes, salt)
    return hash_resultado.decode('utf-8')

@app.post("/verificar")
async def verificar_password(datos: LoginRequest):
    try:
        # Simulación de DB (Aquí es donde luego conectarás tu SQL)
        usuario_db = {
            "nombre": "Leonel", 
            "password_hash": "$2b$12$MS5I.mIRh6yHo7K/WbFr1u.xH.ScCHNHbTbfqhfR6pZkTM/W6nyHu"
        }

        # 1. Validar nombre
        if datos.nombre != usuario_db["nombre"]:
            return {"autenticado": False, "mensaje": "Usuario no encontrado"}

        # 2. Verificación con bcrypt
        p_ingresada_bytes = datos.passwordI.encode('utf-8')
        p_hash_db_bytes = usuario_db["password_hash"].encode('utf-8')

        coincide = bcrypt.checkpw(p_ingresada_bytes, p_hash_db_bytes)

        # 3. Respuesta (Agregamos campos para que tu Dashboard funcione)
        return {
            "usuario": datos.nombre, 
            "autenticado": coincide,
            "rol": "Admin" if coincide else None,
            "plan": "Premium" if coincide else None
        }

    except Exception as e:
        print(f"Error: {e}") # Para ver el error en los logs de Koyeb
        raise HTTPException(status_code=500, detail="Error interno del servidor")