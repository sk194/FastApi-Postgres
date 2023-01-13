from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_db

router = APIRouter(
    prefix="/usuarios",
    tags=['Usuarios']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioOut)
def crear_usuarios(usuarios: schemas.UsuarioCreado, db:Session = Depends(get_db)):
    
    hashed_password = utils.hash(usuarios.password)
    usuarios.password = hashed_password        
    nuevo_usuario = models.Usuario(**usuarios.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/{id}", response_model= schemas.UsuarioOut)
def buscar_usuario(id:int, db:Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if usuario == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"usuario con id= {id} no existe")
    return usuario