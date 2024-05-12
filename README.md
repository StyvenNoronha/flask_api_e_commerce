git push -u origin main
instalar os pacotes 
pip install -r requirements.txt

para criar o banco de dados digita no terminal 
 flask shell
 db.create_all() #criar as tabelas
 db.session.commit() #conexão com o banco
