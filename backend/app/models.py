from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    registros = db.relationship("Registro", backref="usuario", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Registro(db.Model):
    __tablename__ = 'registro'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # 'entrada' o 'salida'
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Registro {self.tipo} by {self.usuario_id} at {self.fecha_hora}>"
