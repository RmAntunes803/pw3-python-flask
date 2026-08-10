#Importando o flask para a aplicação
from flask import  render_template, request, redirect, url_for
# importando o Model de Games
from models.database import Game, db, Console, Usuario
#Importando a biblioteca werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
# hhtps://www.freetogame.com/api/games
import urllib.request #envia requisisçoes para uma URL(endereço online)
import json #converte dados de dicionário para json e vice versa



#Criandoa a função principal para inicializar as rotas
def init_app(app):
    #Variaveis globais
    listaConsoles = ['Playstation 5', 'xbox One', 'Super Nintendo', 'Atari', '3DS',]
    
    listaGames = [{'titulo' : 'CS-GO', 'ano': 2012, 'categoria': 'FPS online', 'plataforma': 'PC (Windows)'}]
    
    
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

    @app.route('/consoles', methods=['GET', 'POST'])
    def consoles():
        # Criando um objeto
        console = {"Nome" : "Playstation 2",
                "Fabricante" : "Sony",
                "Ano" : 2000}
       
        
        #Recebendo o valor do formulário
        if request.method == 'POST':
            if request.form.get('novoConsole'):
                listaConsoles.append(request.form.get('novoConsole'))
                

        return render_template('consoles.html',
                            console = console,
                            listaConsoles = listaConsoles)
        
    @app.route("/cadgames", methods=['GET', 'POST'])
    def cadgames():
        # recebendo os dados do formulario e enviando para pagina
        # verificando se a requisição do usuario é do tipo POST
        if request.method == 'POST':
            # aqui ele ira gravar a lista d ejogos
            listaGames.append({'titulo' : request.form.get('titulo'), 'ano' : request.form.get('ano'), 'categoria' : request.form.get('categoria'), 'plataforma': request.form.get('plataforma')})
            # Aqui o usuário será redireionado novamente para página
            return redirect(url_for('cadgames'))
            
        return render_template('cadgames.html',
                                listaGames = listaGames)
        
        #ROTA PARA O CRUD (ESTOQUE DE JOGOS)
    @app.route('/estoque', methods=['GET', 'POST'])
    #adicionando o parametro id a rota
    @app.route('/estoque/delete;<int:id>')
    def estoque(id=None):
        #verificando se o id foi passado para a rota
        if id:
            game = Game.query.get(id) #seleciona o jogo
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
        #CONDICAO PARA VERIFICAR SE O USUARIO ESTA ENVIANDO UMA REQUISIÇÂO POST (cadstro)
        if request.method == 'POST':
            #REALIZA O CADASTRO
            #COLETANDO OS DADOS DO FORMULARIO
            #Pega os dados do formulario e transforma em um dicionario (objeto)
            dados = request.form.to_dict()
            # Enviando os dados para o Model
            newgame = Game(
                dados['titulo'],
                dados['ano'],
                dados['categoria'],
                dados['plataforma'],
                dados['preco'],
                dados['quantidade']
            )
            # Metodo do SQLAlchemy para gravar no banco
            db.session.add(newgame)
            # Confirmação
            db.session.commit()
            return redirect(url_for('estoque'))
        
        # SELCIONANDO TODOS OS JOGOS DA TABELA
        games = Game.query.all()
        return render_template('estoque.html', games=games)
    
    @app.route('/estoque_console', methods=['GET', 'POST'])
    def estoque_console():
        #CONDICAO PARA VERIFICAR SE O USUARIO ESTA ENVIANDO UMA REQUISIÇÂO POST (cadstro)
        if request.method == 'POST':
            #REALIZA O CADASTRO
            #COLETANDO OS DADOS DO FORMULARIO
            #Pega os dados do formulario e transforma em um dicionario (objeto)
            dados = request.form.to_dict()
            # Enviando os dados para o Model
            newconsole = Console(
                dados['nome'],
                dados['fabricante'],
                dados['ano'],
                dados['preco'],
             
            )
            # Metodo do SQLAlchemy para gravar no banco
            db.session.add(newconsole)
            # Confirmação
            db.session.commit()
            return redirect(url_for('estoque_console'))
        
        # SELCIONANDO TODOS OS JOGOS DA TABELA
        consoles = Console.query.all()
        return render_template('estoque_console.html', consoles=consoles)
    
    @app.route('/estoque/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        #Selecionando o jogo do banco pelo id
        game = Game.query.get(id)
        #Verificando se a requisição é post
        if request.method == 'POST':
            dados_form = request.form.to_dict()
            #alterando os dados do jogo
            game.titulo = dados_form['titulo']
            game.ano = dados_form['ano']
            game.categoria = dados_form['categoria']
            game.plataforma = dados_form['plataforma']
            game.preco = dados_form['preco']
            game.quantidade = dados_form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editGame.html', game=game)
    
    @app.route('/cadastro', methods=['GET' , 'POST'])
    def cadastro():
        if request.method == 'POST':
            #Coleta de dados do formulario
            email = request.form['email']
            senha = request.form['senha']
            #Gerando o hash de senha(CRIPTOGRAFIA)
            senha_com_hash = generate_password_hash(senha, method='scrypt')
            #enviando os dados para model
            novo_usuario = Usuario(email=email, senha=senha_com_hash)
            #gravando no banco
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('cadastro.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    #ROTA DO CONSUMO DA API
    @app.route('/apigames', methods=['GET' , 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        # Variável que armazena URL da API
        url = 'https://www.freetogame.com/api/games'
        req = urllib.request.urlopen(url)
        dados = req.read() #Lendo a resposta da requisição
        #Convertendo a resposta da API de JSON para DICIONARIO
        listaJogos = json.loads(dados)
        
        #verificar se foi passado uma id para rota
        if id:
            jogoInfo = []
            for jogo in listaJogos:
                #VERIFIQUE SE O ID CORRESPONDE 
                if jogo['id'] == id:
                    jogoInfo = jogo
                    #interrompendo
                    break
            if jogoInfo:
                return render_template('jogoInfo.html', jogoInfo=jogoInfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        else:
            return render_template('apigames.html', listaJogos=listaJogos)
    