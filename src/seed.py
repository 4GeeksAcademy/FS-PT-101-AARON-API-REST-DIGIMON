from app import app, db
from models import User, Niño, Digimon, Objeto, Favoritos
from models import Tipo, Atributo

with app.app_context():
    db.drop_all()
    db.create_all()

    # Usuarios creados
    users = [
        User(email="andres@example.com", password="12345"),
        User(email="maria.lopez@example.com", password="abcde"),
        User(email="juan.perez@example.com", password="pass123"),
        User(email="sofia.garcia@example.com", password="qwerty"),
        User(email="carlos.mendez@example.com", password="123abc"),
        User(email="laura.ramirez@example.com", password="98765"),
        User(email="diego.torres@example.com", password="pasword"),
        User(email="ana.morales@example.com", password="1a2b3c"),
        User(email="felipe.navarro@example.com", password="zxcvb")
    ]
    db.session.add_all(users)
    db.session.commit()

    # Niños creados
    niños = [
        Niño(nombre="Tai", apellido="Kamiya",
             edad=11, direccion="Calle Kamikaze 123"),
        Niño(nombre="Matt", apellido="Ishida",
             edad=11, direccion="Avenida Rock 456"),
        Niño(nombre="Sora", apellido="Takenouchi",
             edad=11, direccion="Calle Flor 789"),
        Niño(nombre="Izzy", apellido="Izumi", edad=10,
             direccion="Bulevar Digital 321"),
        Niño(nombre="Mimi", apellido="Tachikawa",
             edad=10, direccion="Pasaje Rosa 654"),
        Niño(nombre="Joe", apellido="Kido", edad=12,
             direccion="Calle Hospital 987"),
        Niño(nombre="T.K.", apellido="Takaishi",
             edad=8, direccion="Calle Ángel 147"),
        Niño(nombre="Kari", apellido="Kamiya",
             edad=8, direccion="Calle Luz 258")
    ]
    db.session.add_all(niños)
    db.session.commit()
    # Digimons creados
    digimons = [
        Digimon(nombre="Agumon", tipo=Tipo.REPTIL,
                atributo=Atributo.VACUNA, altura=1.3, peso=30.0),
        Digimon(nombre="Gabumon", tipo=Tipo.REPTIL,
                atributo=Atributo.VACUNA, altura=1.3, peso=55.0),
        Digimon(nombre="Biyomon", tipo=Tipo.AVE,
                atributo=Atributo.VACUNA, altura=0.9, peso=12.0),
        Digimon(nombre="Tentomon", tipo=Tipo.INSECTO,
                atributo=Atributo.VACUNA, altura=1.0, peso=22.0),
        Digimon(nombre="Palmon", tipo=Tipo.PLANTA,
                atributo=Atributo.VACUNA, altura=0.8, peso=19.0),
        Digimon(nombre="Gomamon", tipo=Tipo.BESTIA,
                atributo=Atributo.VACUNA, altura=1.1, peso=35.0),
        Digimon(nombre="Patamon", tipo=Tipo.MAMIFERO,
                atributo=Atributo.VACUNA, altura=0.5, peso=10.0),
        Digimon(nombre="Gatomon", tipo=Tipo.BESTIA,
                atributo=Atributo.VACUNA, altura=0.6, peso=18.0)
    ]
    db.session.add_all(digimons)
    db.session.commit()
    # objetos creados
    objetos = [
        Objeto(nombre="Emblema del valor", color="naranja"),
        Objeto(nombre="Emblema de la Amistad", color="azul"),
        Objeto(nombre="Emblema del Amor", color="rojo"),
        Objeto(nombre="Emblema del Conocimiento", color="morado"),
        Objeto(nombre="Emblema de la Pureza", color="verde"),
        Objeto(nombre="Emblema de la Sinceridad", color="rosado"),
        Objeto(nombre="Emblema de la Esperanza", color="amarillo"),
        Objeto(nombre="Emblema de la Luz", color="blanco")
    ]
    db.session.add_all(objetos)
    db.session.commit()
    # Favoritos creados
    favoritos = [
        Favoritos(id_user=users[0].id, id_niño=niños[0].id,
                  id_digimon=digimons[0].id, id_objeto=objetos[0].id),
        Favoritos(id_user=users[0].id, id_digimon=digimons[2].id),
        Favoritos(id_user=users[1].id, id_niño=niños[3].id),
        Favoritos(id_user=users[2].id, id_objeto=objetos[1].id),
        Favoritos(id_user=users[3].id, id_niño=niños[2].id,
                  id_digimon=digimons[1].id),
        Favoritos(
            id_user=users[4].id, id_digimon=digimons[0].id, id_objeto=objetos[3].id),
        Favoritos(id_user=users[5].id,
                  id_niño=niños[1].id, id_objeto=objetos[2].id),
        Favoritos(id_user=users[6].id),
        Favoritos(id_user=users[7].id, id_digimon=digimons[4].id),
        Favoritos(id_user=users[8].id, id_niño=niños[0].id,
                  id_digimon=digimons[3].id, id_objeto=objetos[4].id)
    ]
    db.session.add_all(favoritos)
    db.session.commit()

    print("✅ Datos de ejemplo insertados correctamente.")
