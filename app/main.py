from fastapi import FastAPI, HTTPException, Depends
from asyncpg import create_pool, Connection
from pydantic import BaseModel



app = FastAPI()



db_pool = None

# Configura la conexión
DATABASE_URL = "postgresql://midb_ff6g_user:5FebCuwKycGrfFm7NK4l7r8Um7PTfNXY@dpg-cu5bapij1k6c73er76n0-a.oregon-postgres.render.com/midb_ff6g"


@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()

#modelos para fastapi
class Usuario(BaseModel):
      nombre_usuario : str 
      correo:str
      contrasena:str

class Publicacion(BaseModel):
    usuario_id: int
    contenido: str

class Comentario(BaseModel):
    publicacion_id: int
    usuario_id: int
    contenido: str

class Relacion(BaseModel):
    seguidor_id: int
    seguido_id: int


@app.get("/")
async def welcome():
    return {"mensaje": "¡Bienvenido a mi red social!"}

# Endpoints de Usuarios
@app.get("/usuarios/")
async def get_usuarios():
    async with db_pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM usuarios")
        return [dict(row) for row in rows]



@app.post("/usuarios/")
async def create_usuario(usuario: Usuario):
    async with db_pool.acquire() as connection:
        query = """
        INSERT INTO usuarios (nombre_usuario, correo, contrasena)
        VALUES ($1, $2, $3)
        RETURNING id
        """
        user_id = await connection.fetchval(query, usuario.nombre_usuario, usuario.correo, usuario.contrasena)
        return {"id": user_id, "nombre_usuario": usuario.nombre_usuario, "correo": usuario.correo}

# Endpoints de Publicaciones
@app.get("/publicaciones/")
async def get_publicaciones():
    async with db_pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM publicaciones")
        return [dict(row) for row in rows]

@app.post("/publicaciones/")
async def create_publicacion(publicacion: Publicacion):
    async with db_pool.acquire() as connection:
        query = """
        INSERT INTO publicaciones (usuario_id, contenido)
        VALUES ($1, $2)
        RETURNING id
        """
        pub_id = await connection.fetchval(query, publicacion.usuario_id, publicacion.contenido)
        return {"id": pub_id, "usuario_id": publicacion.usuario_id, "contenido": publicacion.contenido}

# Endpoints de Comentarios
@app.get("/comentarios/")
async def get_comentarios():
    async with db_pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM comentarios")
        return [dict(row) for row in rows]

@app.post("/comentarios/")
async def create_comentario(comentario: Comentario):
    async with db_pool.acquire() as connection:
        query = """
        INSERT INTO comentarios (publicacion_id, usuario_id, contenido)
        VALUES ($1, $2, $3)
        RETURNING id
        """
        com_id = await connection.fetchval(query, comentario.publicacion_id, comentario.usuario_id, comentario.contenido)
        return {"id": com_id, "publicacion_id": comentario.publicacion_id, "usuario_id": comentario.usuario_id, "contenido": comentario.contenido}

# Endpoints de Relaciones
@app.get("/relaciones/")
async def get_relaciones():
    async with db_pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM relaciones")
        return [dict(row) for row in rows]

@app.post("/relaciones/")
async def create_relacion(relacion: Relacion):
    async with db_pool.acquire() as connection:
        query = """
        INSERT INTO relaciones (seguidor_id, seguido_id)
        VALUES ($1, $2)
        RETURNING id
        """
        rel_id = await connection.fetchval(query, relacion.seguidor_id, relacion.seguido_id)
        return {"id": rel_id, "seguidor_id": relacion.seguidor_id, "seguido_id": relacion.seguido_id}