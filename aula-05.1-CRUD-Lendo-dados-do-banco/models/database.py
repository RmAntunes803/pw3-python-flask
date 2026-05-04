# importando o flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Carregando o SQLAlchemy em uma variável
db = SQLAlchemy()

# Criando uma classe para representar a entidade Games no banco
# Nome de classe sempre no singular(boa pratica)
class Game(db.Model):
    # Definindo os atributos (colunas) da tabela
    # Schema (estrutura a baixo)
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    ano = db.Column(db.Integer)
    categoria = db.Column(db.String(150))
    plataforma = db.Column(db.String(150))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    
    # Incializando as variáveis a classe (metodo construtor)
    #self parametro que significa a si mesmo
    def __init__(self, titulo, ano, categoria, plataforma, preco, quantidade):
        self.titulo = titulo
        self.ano = ano
        self.categoria = categoria
        self.plataforma = plataforma
        self.preco = preco 
        self.quantidade = quantidade
        
