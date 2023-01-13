from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class PosteoBase(BaseModel):
    titulo: str
    contenido: str
    publicado: bool = True
    
class CrearPosteo(PosteoBase):
    pass

class UsuarioOut(BaseModel):
    id: int
    email: EmailStr
    creado: datetime
    
    class Config:
      orm_mode = True
      

class Posteo(PosteoBase):
    id: int
    # titulo: str
    # contenido: str
    # publicado: bool
    creado : datetime
    owner_id: int
    owner: UsuarioOut 
    
    class Config:
      orm_mode = True
      
class PosteoOut(BaseModel):
    Posteo: Posteo
    votos : int
    
    class Config:
      orm_mode = True
      
class UsuarioCreado(BaseModel):
    email: EmailStr
    password: str
    

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Voto(BaseModel):
    posteo_id: str
    dir: conint(le=1)
