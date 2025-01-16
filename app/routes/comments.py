from fastapi import APIRouter, HTTPException

router = APIRouter()

# Simularemos una lista de comentarios como base de datos temporal
comments_db = []

# Crear un comentario
@router.post("/", response_model=dict)
async def create_comment(content: str, user_id: int, post_id: int):
    comment_id = len(comments_db) + 1
    comment = {
        "id": comment_id,
        "content": content,
        "user_id": user_id,
        "post_id": post_id,
    }
    comments_db.append(comment)
    return {"message": "Comentario creado exitosamente", "comment": comment}


# Obtener todos los comentarios
@router.get("/", response_model=list)
async def get_comments():
    return comments_db


# Obtener un comentario por ID
@router.get("/{comment_id}", response_model=dict)
async def get_comment(comment_id: int):
    for comment in comments_db:
        if comment["id"] == comment_id:
            return comment
    raise HTTPException(status_code=404, detail="Comentario no encontrado")


# Eliminar un comentario
@router.delete("/{comment_id}", response_model=dict)
async def delete_comment(comment_id: int):
    global comments_db
    comments_db = [comment for comment in comments_db if comment["id"] != comment_id]
    return {"message": "Comentario eliminado exitosamente"}