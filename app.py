from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
#CHAVE DO BANCO DE DADOS
app.config['SECRET_KEY'] = "your_secret_key"
#CAMINHO BANCO DE DADOS9k
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3307/flask-crud' #bd sql + lib pymysql

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
#view login
login_manager.login_view = 'login' #rota do login para funcionar

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    #credenciais
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
       #LOGANDO
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):#autenticação
                login_user(user)
                print(current_user.is_authenticated)
                return jsonify({"message":"Autenticação realizada com sucesso"})
    return jsonify({"message":"Credenciais inválidas"}), 400


@app.route('/logout', methods=['GET'])
@login_required#apenas para quem fez login, caso não dara erro
def logout():
     logout_user()
     return jsonify({"message": "Logout realizado com sucesso"})


@app.route('/user',methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password),bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message" : "Usuario cadastrado com sucesso!"})
     
    return jsonify({"message" : "Dados inválidos!"}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
     user = User.query.get(id_user)

     if user:
          return {"username": user.username}
     return jsonify({"message": "Usuario não encontrado"}),404

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
     data = request.json
     user = User.query.get(id_user)

     if id_user != current_user.id and current_user.role == "user":
          return jsonify({"message": "Operação não permitida"}), 403

     if user and data.get("password"):
          user.password = data.get("password") 
          db.session.commit()
          return jsonify({"message": f"Usuario:{id_user} atualizado com sucesso"})
     return jsonify({"message": "Usuario não encontrado"}),404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    
    if current_user.role != 'admin':
         return jsonify({"message":"Operação não permitida"}),403
    if id_user == current_user.id:#evita de remover a si mesmo
         return jsonify({"message": "Deleção não permitida"}),403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuario:{id_user} deletado com sucesso"})
    return jsonify({"message": "Usuario não encontrado"}),404


#testando o flask
@app.route("/hello-word", methods=["GET"])
def hello_word():
    return "Olá Mundo"

#DEBUG LOCAL
if __name__ == '__main__':
    app.run(debug=True)