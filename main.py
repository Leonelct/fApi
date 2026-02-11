from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt
from typing import Optional

app = FastAPI()

# --- CONFIGURACIÓN DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- BASE DE DATOS SIMULADA ---
# Añadimos los roles aquí para que el sistema pueda consultarlos
usuarios_db = {
    "Leonel": {
        "password_hash": "$2b$12$MS5I.mIRh6yHo7K/WbFr1u.xH.ScCHNHbTbfqhfR6pZkTM/W6nyHu",
        "rol": "Administrador",
        "plan": "Empresarial",
        "status": "Activo"
    },
    "Invitado": {
        "password_hash": "$2b$12$...", # Hash real aquí
        "rol": "Usuario",
        "plan": "Básico",
        "status": "Limitado"
    }
}

# --- MODELOS ---
class LoginRequest(BaseModel):
    username: str
    password: str

# --- MIDDLEWARE / DEPENDENCIAS DE CONTROL DE ACCESO ---

# Esta función verifica si el usuario existe (autenticación básica)
async def obtener_usuario_actual(username: str):
    user = usuarios_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"username": username, **user}

# Esta función es el "Guardia" que solo deja pasar a Administradores
async def verificar_es_admin(usuario=Depends(obtener_usuario_actual)):
    if usuario["rol"] != "Administrador":
        raise HTTPException(
            status_code=403, 
            detail="Acceso denegado: No tienes permisos de Administrador"
        )
    return usuario

# --- RUTAS ---

@app.post("/verificar")
async def verificar_password(datos: LoginRequest):
    try:
        user_info = usuarios_db.get(datos.username)
        if not user_info:
            return {"autenticado": False, "mensaje": "Usuario no encontrado"}

        p_ingresada_bytes = datos.password.encode('utf-8')
        p_hash_db_bytes = user_info["password_hash"].encode('utf-8')

        coincide = bcrypt.checkpw(p_ingresada_bytes, p_hash_db_bytes)

        return {
            "usuario": datos.username, 
            "autenticado": coincide
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# RUTA PROTEGIDA: Solo usuarios logueados pueden ver perfiles
@app.get("/perfil/{username}")
async def obtener_perfil(username: str, current_user=Depends(obtener_usuario_actual)):
    perfil = usuarios_db.get(username)
    return {
        "username": username,
        "rol": perfil["rol"],
        "plan": perfil["plan"],
        "status": perfil["status"]
    }

# RUTA SÚPER PROTEGIDA: Solo el rol 'Administrador' puede entrar aquí
@app.get("/admin/panel-control")
async def panel_admin(admin=Depends(verificar_es_admin)):
    return {
        "mensaje": f"Bienvenido al panel secreto, {admin['username']}",
        "usuarios_totales": len(usuarios_db),
        "servidor": "Koyeb Pro"
    }