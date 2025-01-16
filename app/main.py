from fastapi import FastAPI
from app.db import database
from app.routes import users, posts, comments

# Crea la instancia de la aplicación FastAPI
app = FastAPI()

# Conexión a la base de datos (al iniciar la app)
@app.on_event("startup")
async def startup():
    # Conecta a la base de datos
    await database.connect()

# Desconexión de la base de datos (al cerrar la app)
@app.on_event("shutdown")
async def shutdown():
    # Desconecta de la base de datos
    await database.disconnect()

# Rutas principales
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello, Database API"}

# Rutas de usuarios
app.include_router(users.router, prefix="/users", tags=["Users"])

# Rutas de publicaciones
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

# Rutas de comentarios
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
