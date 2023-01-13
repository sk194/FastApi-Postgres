from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .routers import post, usuario, auth, voto
from .config import settings

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()   

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# mis_posteos = [{"title": "titulo post1", "content": "contenido de post 1", "id": 1},
#                {"title": "titulo comida favorita", "content": "me gusta la pizaa", "id": 2}
#               ]  

        
app.include_router(post.router)
app.include_router(usuario.router)
app.include_router(auth.router)
app.include_router(voto.router)

               
@app.get("/")
def root():
    return {"message": "Bienvenido a la API!!"}




        
