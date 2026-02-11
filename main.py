from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # ELIMINADA LA BARRA FINAL: 'http://localhost:5173' en lugar de 'http://localhost:5173/'
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debe coincidir con las llaves que envías en el JSON de React
class LoginRequest(BaseModel):
    username: str # Antes era 'nombre'
    password: str # Antes era 'passwordI'

@app.post("/verificar")
async def verificar_password(datos: LoginRequest):
    try:
        usuario_db = {
            "nombre": "Leonel", 
            "password_hash": "$2b$12$MS5I.mIRh6yHo7K/WbFr1u.xH.ScCHNHbTbfqhfR6pZkTM/W6nyHu",
            "rol": "Admin",
            "plan": "Premium",
        }

        # 1. Validar nombre (comparamos con datos.username ahora)
        if datos.username != usuario_db["nombre"]:
            return {"autenticado": False, "mensaje": "Usuario no encontrado"}

        # 2. Verificación con bcrypt (usamos datos.password ahora)
        p_ingresada_bytes = datos.password.encode('utf-8')
        p_hash_db_bytes = usuario_db["password_hash"].encode('utf-8')

        coincide = bcrypt.checkpw(p_ingresada_bytes, p_hash_db_bytes)

        return {
            "usuario": datos.username, 
            "autenticado": coincide,
            "rol": "Admin" if coincide else None,
            "plan": "Premium" if coincide else None
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/perfil/{username}")
async def obtener_perfil(username: str):
    # En el futuro, aquí buscarías en SQL. Por ahora simulamos la DB:
    usuarios_db = {
        "Leonel": {"rol": "Administrador", "plan": "Empresarial", "status": "Activo"},
        "Invitado": {"rol": "Usuario", "plan": "Básico", "status": "Limitado"}
    }
    
    perfil = usuarios_db.get(username)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    
    return {
        "username": username,
        "rol": perfil["rol"],
        "plan": perfil["plan"],
        "status": perfil["status"]
    }