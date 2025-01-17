from fastapi import FastAPI, HTTPException, Depends
from asyncpg import create_pool, Connection
from pydantic import BaseModel

app = FastAPI()

# Configura la conexión
DATABASE_URL = "postgresql://midb_ff6g_user:5FebCuwKycGrfFm7NK4l7r8Um7PTfNXY@dpg-cu5bapij1k6c73er76n0-a.oregon-postgres.render.com/midb_ff6g"
db_pool = None

@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()

# Modelo para insertar datos
class Item(BaseModel):
    nombre: str
    descripcion: str

class Usuario(BaseModel):
    nombre: str
    email: str

# Obtener todos los datos
@app.get("/items/")
async def get_items():
    async with db_pool.acquire() as connection:  # Adquiere conexión del pool
        rows = await connection.fetch("SELECT * FROM items")
        return [dict(row) for row in rows]

# Obtener un dato por ID
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    async with db_pool.acquire() as connection:
        row = await connection.fetchrow("SELECT * FROM items WHERE id = $1", item_id)
        if not row:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        return dict(row)

# Insertar un nuevo dato
@app.post("/items/")
async def create_item(item: Item):
    async with db_pool.acquire() as connection:
        query = "INSERT INTO items (nombre, descripcion) VALUES ($1, $2) RETURNING id"
        item_id = await connection.fetchval(query, item.nombre, item.descripcion)
        return {"id": item_id, "nombre": item.nombre, "descripcion": item.descripcion}

# Actualizar un dato
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    async with db_pool.acquire() as connection:
        query = """
        UPDATE items
        SET nombre = $1, descripcion = $2
        WHERE id = $3
        RETURNING id
        """
        updated_id = await connection.fetchval(query, item.nombre, item.descripcion, item_id)
        if not updated_id:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        return {"id": updated_id, "nombre": item.nombre, "descripcion": item.descripcion}

# Eliminar un dato
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    async with db_pool.acquire() as connection:
        query = "DELETE FROM items WHERE id = $1 RETURNING id"
        deleted_id = await connection.fetchval(query, item_id)
        if not deleted_id:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        return {"detail": f"Item con id {deleted_id} eliminado exitosamente"}





# crud de usuarios 
@app.get("/usuarios/")
async def get_users():
    async with db_pool.acquire() as connection:  # Adquiere conexión del pool
        rows = await connection.fetch("SELECT * FROM usuarios")
        return [dict(row) for row in rows]
    

# Insertar un nuevo dato
@app.post("/usuarios/")
async def create_users(user: Usuario):
    async with db_pool.acquire() as connection:
        query = "INSERT INTO usuarios (nombre, email) VALUES ($1, $2) RETURNING id"
        user_id = await connection.fetchval(query, user.nombre, user.email)
        return {"id": user_id, "nombre": user.nombre, "email": user.email}
