from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#ligação com o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)
#///////
#banco de dados
#classe de produtos
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text, nullable=True)


#rotas
#cadastro de produtos
@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data.get("name","erro"), price=data.get("price","erro"),description=data.get("description","erro") )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"produto cadastrado com sucesso"}), 200   
    else:
        return jsonify({"message":"produto invalido"}), 400

#deletar produtos
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"produto deletado com sucesso","NOME":product.name,}), 200   
    else:
        return jsonify({"message":"produto não encontrado"}), 400 
    
    
       
#rota de achar um produto
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)  
    if product:
        return jsonify({"ID":product.id,"NOME":product.name,"PRECO":product.price,"DESCRICAO":product.description}), 200
    else:
        return jsonify({"message": "produto não encontrado"}),400
    
    
#rota de atualização 
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def ypdate_product(product_id):
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
    
             
@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True)    
