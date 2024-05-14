from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
app = Flask(__name__)
app.config['SECRET_KEY'] = "senhasuperdificil"
#ligação com o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)



#///////
#banco de dados
#tabela de usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)  
    
    
    
#tabela de produtos
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text, nullable=True)


#rotas
#autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
##########################################################################################

#login no sistema
@app.route('/login/',methods=["POST"])
def login():
    data = request.json
    
    user = User.query.filter_by(username=data.get("username")).first()
    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message":"Entrou no sistema"})
    return jsonify({"message":"Senha ou usuario incorretos"})  
##########################################################################################
#sair do sistema
@app.route('/logout/', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message":"saiu no sistema"})  
#cadastro de produtos
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data.get("name","erro"), price=data.get("price","erro"),description=data.get("description","erro") )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"produto cadastrado com sucesso"}), 200   
    else:
        return jsonify({"message":"produto invalido"}), 400
##########################################################################################
    
#cadastro de usuarios
@app.route('/api/user/add', methods=["POST"])
@login_required
def add_user():
    data = request.json
    if 'username' in data and 'password' in data:
        user = User(username=data.get("username","erro"), password=data.get("password","erro"))
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"Usuario cadastrado com sucesso"}), 200   
    else:
        return jsonify({"message":"Erro ao adicionar um usuario"}), 400    
##########################################################################################

#deletar produtos
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"produto deletado com sucesso","NOME":product.name,}), 200   
    else:
        return jsonify({"message":"produto não encontrado"}), 400 
##########################################################################################
      
#rota de achar um produto
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)  
    if product:
        return jsonify({"ID":product.id,"NOME":product.name,"PRECO":product.price,"DESCRICAO":product.description}), 200
    else:
        return jsonify({"message": "produto não encontrado"}),400
##########################################################################################
   
#rota de atualização 
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "produto não encontrado"}),400
    data = request.json
    if 'name' in data:
        product.name = data['name']
    
    if 'price' in data:
        product.price = data['price']    
        
    if 'description' in data:
        product.description = data['description']    
    db.session.commit()
    return jsonify({"messager":"Produto atualizado com sucesso"}), 200
##########################################################################################

#lista dos produtos
@app.route('/api/products', methods=["GET"])
def get_product():
    products = Product.query.all()
    product_list = []
    for p in products:
        product_data = {"ID":p.id,"NOME":p.name,"PRECO":p.price,"DESCRICAO":p.description}
        product_list.append(product_data)
    return jsonify(product_list)
##########################################################################################
             
@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True)    
##########################################################################################
