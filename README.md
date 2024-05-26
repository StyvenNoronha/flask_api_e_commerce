git push -u origin main
instalar os pacotes 
pip install -r requirements.txt

para criar o banco de dados digita no terminal 
 flask shell
 db.create_all() #criar as tabelas
 db.session.commit() #conexão com o banco

 para criar o banco de dados digita no terminal 
 flask shell
 db.drop_all()          #Apaga todas as tabelas no banco
 db.create_all()        #Criar todas as tabelas
 db.session.commit()    #Conexão com o banco
 exit()                 #sair do shell

 user= User(username="admin", password="123") 
 db.session.add(user)
 db.session.commit()

 