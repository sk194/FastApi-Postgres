from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Posteo(Base):
    __tablename__ = "posteos"
    
    id = Column(Integer, primary_key=True, nullable=False)
    titulo = Column(String, nullable=False)
    contenido = Column(String, nullable=False)
    publicado = Column(Boolean, server_default='TRUE', nullable=False)
    creado = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )
    owner_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable= False)
    
    owner = relationship("Usuario")
    
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique= True)
    password = Column(String, nullable=False)
    creado = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )
    
class Voto(Base):
    __tablename__ = "votos"
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    posteo_id = Column(Integer, ForeignKey("posteos.id", ondelete="CASCADE"), primary_key=True)