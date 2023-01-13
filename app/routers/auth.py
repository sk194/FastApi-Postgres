from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Auntenticación']
)

@router.post('/login', response_model=schemas.Token)
def login(usuario_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == usuario_credentials.username).first()
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Credenciales inválidas')
    
    if not utils.verificar(usuario_credentials.password, usuario.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Credenciales inválidas')

        
    # crear token
    access_token = oauth2.crear_access_token(data= {"usuario_id": usuario.id})
    # retornar token
    return {"access_token": access_token, "token_type": "bearer"}