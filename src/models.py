from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from enum import Enum

db = SQLAlchemy()

class Atributo(str, Enum):
    VACUNA = "vacuna"
    VIRUS = "virus"
    INFORMACION = "informacion"

class Tipo(str, Enum):
    REPTIL = "reptil"
    AVE = "ave"
    INSECTO = "insecto"
    PLANTA = "planta"
    BESTIA = "bestia"
    MAMIFERO = "mamifero"
    DRAGON = "dragon"

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    favoritos: Mapped[list["Favoritos"]] = relationship(back_populates="usuario")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Niño(db.Model):
    __tablename__ = "niños"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    apellido: Mapped[str] = mapped_column(String(120), nullable=False)
    edad: Mapped[int] = mapped_column(nullable=False)
    direccion: Mapped[str] = mapped_column(String(120))

    ##Aqui va la relacion con la tabla fav

    favoritos: Mapped[list["Favoritos"]] = relationship(back_populates="niño")

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "direccion": self.direccion
        }
class Digimon(db.Model):
    __tablename__ = "digimons"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[Tipo] = mapped_column(SQLEnum(Tipo), nullable=False)
    atributo: Mapped[Atributo] = mapped_column(SQLEnum(Atributo), nullable=False)
    altura: Mapped[float] = mapped_column(nullable=False)
    peso: Mapped[float] = mapped_column(nullable=False)

    ##Aqui va la relacion con la tabla fav
    favoritos: Mapped[list["Favoritos"]] = relationship(back_populates="digimon")

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "atributo": self.atributo,
            "altura": self.altura,
            "peso": self.peso
        }
class Objeto(db.Model):
    __tablename__ = "objetos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    color: Mapped[str] = mapped_column(String(120), nullable=False)

    ##Aqui va la relacion con la tabla fav
    favoritos: Mapped[list["Favoritos"]] = relationship(back_populates="objeto")

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "color": self.color
        }
class Favoritos(db.Model):
    __tablename__ = "favoritos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    id_niño: Mapped[int] = mapped_column(ForeignKey("niños.id"), nullable=True)
    id_digimon: Mapped[int] = mapped_column(ForeignKey("digimons.id"), nullable=True)
    id_objeto: Mapped[int] = mapped_column(ForeignKey("objetos.id"), nullable=True)

    #relaciones
    usuario: Mapped["User"] = relationship(back_populates="favoritos")
    niño: Mapped["Niño"] = relationship(back_populates="favoritos")
    digimon: Mapped["Digimon"] = relationship(back_populates="favoritos")
    objeto: Mapped["Objeto"] = relationship(back_populates="favoritos")

    def serialize(self):
        return{
            "id_user": self.id_user,
            "id_niño": self.id_niño,
            "id_digimon": self.id_digimon,
            "id_objeto" : self.id_objeto
        }
    


