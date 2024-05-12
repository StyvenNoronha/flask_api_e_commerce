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

    
    
@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == "__main__":
    app.run(debug=True)    
