import pytest
from src.app import create_app, db, Role, User

@pytest.fixture
def app():
    app = create_app({
        "SECRET_KEY": 'test',
        "SQLALCHEMY_DATABASE_URI": 'sqlite://',
        "JWT_SECRET_KEY" :  'test',
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def access_token(client):
    # Criação da role ADMINISTRADOR
    role = Role(name="administrador")
    db.session.add(role)
    db.session.commit()

    # Criação do Usuario
    user = User(username = "John-doe", password="test", role_id=role.id )
    db.session.add(user)
    db.session.commit()

    response= client.post("/auth/login", json= {"username": user.username, "password": user.password}) # Faz a autenticação do usuario
    return response.json["access_token"] # Recupera o token de autenticação