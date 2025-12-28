from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin # Gestión de sesion,El uso de UserMixin proporciona métodos como is_authenticated() y get_id(), esenciales para la autenticación
from flask_bcrypt import Bcrypt # Encripta claves
from configs import app
#Instancio la app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../src/agenda.db'
app.secret_key = 'AgendaTest2025'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


#Clases para armar las tables y modelos
class Clientes(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    tel = db.Column(db.String(10))
    dom = db.Column(db.String(50))

class Trabajos(db.Model):
    __tablename__ = 'trabajo'
    id = db.Column(db.Integer, primary_key=True)
    id_cli =  db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    tarea = db.Column(db.Text, nullable=False)
    sol = db.Column(db.Text)
    total = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

class Usuarios(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    rol = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False)
    
    def is_authenticated(self):
	    return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    def is_admin(self):
        return self.admin