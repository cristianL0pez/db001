from typing import List  # Importar List para versiones de Python anteriores
from fastapi import APIRouter, HTTPException
from app import crud, schemas

router = APIRouter()

# Crear publicación
@router.post("/", response_model=schemas.PostOut)
async def create_post(post: schemas.PostCreate, user_id: int):
    post_data = await crud.create_post(post, user_id)
    return post_data


# Obtener todas las publicaciones
@router.get("/", response_model=List[schemas.PostOut])  # Cambiar list por List
async def get_posts():
    return await crud.get_posts()


# Obtener publicación por ID
@router.get("/{post_id}", response_model=schemas.PostOut)
async def get_post(post_id: int):
    post = await crud.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return post