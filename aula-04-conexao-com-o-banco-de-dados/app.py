#Comentario no python

#Importando o flask para a aplicação
from flask import Flask, render_template

#Importando o PYMYSQL
import pymysql
# Importando o SQLAlchemy e o MODEL
from models.database import db, Game

#Definindo um nome para o banco
DB_NAME = 'thegames'


#Importando o Controller
from controllers import routes
#carregando o Flask na variavel "app"
#declarando variavel no python
app = Flask(__name__, template_folder='views')
#variaveis com __ são variaveis de ambiente do python
#__name__ representa o nome da aplicação

# Passando o nome do banco para o flask
app.config['DATABASE_NAME'] = DB_NAME
# Passando o endereço do banco para o Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

#Enviando a variável app para as rotas
routes.init_app(app)





#iniciando o servidor na porta 5000
if __name__ == '__main__':
    # Conectando-se ao MYSQL para criar o banco de dados
    # Passando os dados de conexão
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    #tentando a conexão
    try:
        with connection.cursor() as cursor:
            # Enviando a QUERY para criar o banco
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            print("o banco de dados está criado!")
    except Exception as error:
        print(f"Ocorreu um erro ao criar o banco de dados!' {error}")
    #Fechando a conexão
    finally:
        connection.close()
        
    # Inicializando o FLASK-SQLAlchemy
    db.init_app(app=app)
    # Enviando a requisição para criar as tabelas
    with app.test_request_context():
        db.create_all()
        
    #Inicializando o servidor:
    app.run(port=5000, debug=True)
# o metodo .run() inicia o servidor