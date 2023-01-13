from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posteos']
)


@router.get("/", response_model=List[schemas.PosteoOut])
def get_posts(db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_usuario),
              limit: int=10, skip: int = 0, search: Optional[str] =""):
    # cursor.execute(""" SELECT * FROM posteos """)
    # posteos = cursor.fetchall()
    # print(posteos)
    # posteos = db.query(models.Posteo).filter(
    #     models.Posteo.owner_id == current_user.id).all()
    #posteos = db.query(models.Posteo).filter(models.Posteo.titulo.contains(search)).limit(limit).all()
    
    resultados = db.query(models.Posteo, func.count(models.Voto.posteo_id).label("votos")).join(
        models.Voto, models.Voto.posteo_id == models.Posteo.id, isouter=True).group_by(
        models.Posteo.id).filter(models.Posteo.titulo.contains(search)).limit(
        limit).offset(skip).all()
            
        
        
    # print(resultados)
    return resultados


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Posteo)
def create_posts(posteo: schemas.CrearPosteo, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_usuario)):
    
    # cursor.execute(""" INSERT INTO posteos (titulo,contenido,publicado) VALUES (%s,%s,%s)
    #                RETURNING * """,
    #               (posteo_nuevo.titulo,posteo_nuevo.contenido,posteo_nuevo.publicado))
    # nuevo_posteo= cursor.fetchone()
    # print(posteo_nuevo)
    # posteo_dict = posteo_nuevo.dict()
    # posteo_dict['id'] = randrange(0, 1000000)
    # print(posteo_nuevo.dict())
    # mis_posteos.append(posteo_dict)
    # 
    # nuevo_posteo = models.Posteo(titulo=posteo.titulo,contenido=posteo.contenido,publicado=posteo.publicado)
    # print(current_user.email)
    print(current_user.id)
    nuevo_posteo = models.Posteo(owner_id=current_user.id, **posteo.dict())
    db.add(nuevo_posteo)
    db.commit()
    db.refresh(nuevo_posteo)
    return nuevo_posteo

# def encuentra_post(id):
#     for p in mis_posteos:
#         if p['id'] == id:
#             return p

@router.get("/{id}", response_model=schemas.PosteoOut)
def get_post(id:int, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_usuario)):
    # print(id)
    # cursor.execute(""" SELECT * FROM posteos WHERE id = %s """, (str(id)))
    # posteo = cursor.fetchone()
    # print(test_posteo)
    # posteo = encuentra_post(id)
    #posteo = db.query(models.Posteo).filter(models.Posteo.id == id).first()
    
    posteo = db.query(models.Posteo, func.count(models.Voto.posteo_id).label("votos")).join(
        models.Voto, models.Voto.posteo_id == models.Posteo.id, isouter=True).group_by(
        models.Posteo.id).first()
    if not posteo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"posteo {id} no fue encontrado")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"mensaje": f'posteo {id} no fue encontrado'}
        
    
    return posteo

""" @app.get("/posts/ultimo")
def get_ultimo_posteo():
    posteo = mis_posteos[len(mis_posteos)-1]
    return {"detalle": posteo} """
    
# def encontrar_index_post(id):
#     for i, p in enumerate(mis_posteos):
#         if p['id'] == id:
#             return i
        
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_posteo(id:int, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_usuario)):
    
    # cursor.execute(""" DELETE FROM posteos WHERE id= %s returning*""", (str(id),))
    # eliminar_posteo = cursor.fetchone()
    # conn.commit()
    posteo_query = db.query(models.Posteo).filter(models.Posteo.id == id)
    
    posteo = posteo_query.first()
    
    if posteo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"posteo con id= {id} no existe")
        
    if posteo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No autorizado para realizar la solicitud")
    
    posteo_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Posteo)
def actualizar_posteo(id:int, posteo_actualizado: schemas.CrearPosteo, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_usuario) ):
    # cursor.execute(""" UPDATE posteos SET titulo= %s, contenido= %s, publicado= %s WHERE id= %s returning*""",
    #                (posteo.titulo, posteo.contenido, posteo.publicado, str(id)))
    # actualizar_posteo = cursor.fetchone()
    # conn.commit()
    posteo_query = db.query(models.Posteo).filter(models.Posteo.id == id)
    posteo = posteo_query.first()
    if posteo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"posteo con id= {id} no existe")
    
    if posteo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No autorizado para realizar la solicitud")
        
    posteo_query.update(posteo_actualizado.dict(), synchronize_session=False)   
    db.commit()
    """ posteo_dict = posteo.dict()
    posteo_dict['id'] = id
    mis_posteos[index] = posteo_dict """
    return posteo_query.first()