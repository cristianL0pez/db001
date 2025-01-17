from fastapi import FastAPI, HTTPException, Depends
from asyncpg import create_pool, Connection
from pydantic import BaseModel

app = FastAPI()

# Configura la conexión
DATABASE_URL = "postgresql://midb_m1sa_user:JUSBmmX4XqnrniLwZLq4yrDd87KS2mBG@dpg-cu4nm8ogph6c73c1qmeg-a.oregon-postgres.render.com/midb_m1sa"
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
