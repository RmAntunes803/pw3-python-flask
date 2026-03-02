#Comentario no python

#Importando o flask para a aplicação
from flask import Flask, render_template
#carregando o Flask na variavel "app"
#declarando variavel no python
app = Flask(__name__, template_folder='views')
#variaveis com __ são variaveis de ambiente do python
#__name__ representa o nome da aplicação

#CRIANDO A ROTA PRINCIPAL DO SITE
@app.route('/')
#def cria funções no python ]
def home():
    return render_template('index.html')
@app.route('/games')
def games():
    # Criando  variáveis para a rota de games
    titulo = "Portal 2"
    ano = 2011
    categoria = "Puzzle"
    #Lista de jogadores (uma lista é um vetor/array)
    jogadores = ['Marcos', 'Richard', 'Miguel', 'Renato', 'Pedro']
    # enviando as variaveis para op html
    
    return render_template('games.html',
                           titulo = titulo,
                           ano = ano,
                           categoria = categoria,
                           jogadores=jogadores )

@app.route('/consoles')
def consoles():
    # Criando um objeto
    console = {"Nome" : "Playstation 2",
               "Fabricante" : "Sony",
               "Ano" : 2000}
    return render_template('consoles.html',
                           console = console)


#iniciando o servidor na porta 5000
if __name__ == '__main__':
# if esta verificando se o arquivo gravado em __name__ é o arquivo prinicipal
    app.run(port=5000, debug=True)
# o metodo .run() inicia o servidor