from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/voto",
    tags=['Votos']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def voto(voto: schemas.Voto, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_usuario)):
    
    posteo = db.query(models.Posteo).filter(models.Posteo.id == voto.posteo_id).first()
    
    if not posteo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"posteo con id: {voto.posteo_id} no existe")
    
    voto_query = db.query(models.Voto).filter(models.Voto.posteo_id == voto.posteo_id,
                                            models.Voto.usuario_id == current_user.id)
    
    voto_encontrado = voto_query.first()
    
    if (voto.dir == 1):
        if voto_encontrado:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"usuario {current_user.id} ya tiene un voto en el posteo {voto.posteo_id}")
        
        nuevo_voto = models.Voto(posteo_id = voto.posteo_id, usuario_id = current_user.id)
        db.add(nuevo_voto)
        db.commit()
        return{"msj": "Voto agregado"}
    else:
        if not voto_encontrado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voto no existe")
        
        voto_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
    
