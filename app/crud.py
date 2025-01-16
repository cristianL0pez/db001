from app.db import database
from app import schemas
from sqlalchemy import text

# ---------------------------
# Funciones CRUD para Usuarios
# ---------------------------

# Crear un nuevo usuario
async def create_user(user: schemas.UserCreate):
    query = text("""
    INSERT INTO users (username, email, hashed_password)
    VALUES (:username, :email, :hashed_password)
    RETURNING id, username, email;
    """)
    values = {"username": user.username, "email": user.email, "hashed_password": user.password}
    result = await database.fetch_one(query, values)
    return result
# Función CRUD para obtener un usuario por su correo electrónico
async def get_user_by_email(email: str):
    query = text("SELECT * FROM users WHERE email = :email")
    result = await database.fetch_one(query, {"email": email})
    return result

# Obtener un usuario por su ID
async def get_user(user_id: int):
    query = text("SELECT * FROM users WHERE id = :id")
    result = await database.fetch_one(query, {"id": user_id})
    return result

# ---------------------------
# Funciones CRUD para Publicaciones
# ---------------------------

# Crear una nueva publicación
async def create_post(post: schemas.PostCreate, user_id: int):
    query = text("""
    INSERT INTO posts (title, content, user_id)
    VALUES (:title, :content, :user_id)
    RETURNING id, title, content, user_id;
    """)
    values = {"title": post.title, "content": post.content, "user_id": user_id}
    result = await database.fetch_one(query, values)
    return result

# Obtener todas las publicaciones
async def get_posts():
    query = text("SELECT * FROM posts")
    result = await database.fetch_all(query)
    return result

# ---------------------------
# Funciones CRUD para Comentarios
# ---------------------------

# Crear un nuevo comentario
async def create_comment(comment: schemas.CommentCreate):
    query = text("""
    INSERT INTO comments (content, post_id, user_id)
    VALUES (:content, :post_id, :user_id)
    RETURNING id, content, post_id, user_id;
    """)
    values = {"content": comment.content, "post_id": comment.post_id, "user_id": comment.user_id}
    result = await database.fetch_one(query, values)
    return result

# Obtener comentarios por publicación
async def get_comments_by_post(post_id: int):
    query = text("SELECT * FROM comments WHERE post_id = :post_id")
    result = await database.fetch_all(query, {"post_id": post_id})
    return result