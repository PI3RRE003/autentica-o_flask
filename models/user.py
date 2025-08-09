from database import db
from flask_login import UserMixin #autenticação login

class User(db.Model,UserMixin):#tudo que tem no model e mixin
    #colunas id(int), username(text), password(text)
    id = db.Column(db.Integer, primary_key=True) #chave primaria = unica
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')