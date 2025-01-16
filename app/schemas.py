from pydantic import BaseModel, EmailStr
from typing import Optional, List


# ---------------------------
# Esquema de Usuario (User)
# ---------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str  # Contraseña para el registro


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


# ---------------------------
# Esquema de Publicación (Post)
# ---------------------------
class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    user_id: int  # ID del usuario que creó el post

    class Config:
        orm_mode = True


# ---------------------------
# Esquema de Comentario (Comment)
# ---------------------------
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int
    user_id: int  # ID del usuario que comenta


class CommentOut(CommentBase):
    id: int
    post_id: int
    user_id: int

    class Config:
        orm_mode = True


# ---------------------------
# Relación entre entidades
# ---------------------------
class PostWithComments(PostOut):
    comments: List[CommentOut] = []

    class Config:
        orm_mode = True