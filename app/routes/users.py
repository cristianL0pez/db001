from fastapi import APIRouter, HTTPException
from app import crud, schemas
from app.db import database
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Registro de usuario
@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate):
    existing_user = await crud.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    
    hashed_password = pwd_context.hash(user.password)
    user_data = await crud.create_user(schemas.UserCreate(**user.dict(), password=hashed_password))
    return user_data


# Login de usuario
@router.post("/login")
async def login(user: schemas.UserCreate):
    db_user = await crud.get_user_by_email(user.email)
    if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"message": "Inicio de sesión exitoso"}