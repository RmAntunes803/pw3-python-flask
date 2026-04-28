#Importando o flask para a aplicação
from flask import  render_template, request, redirect, url_for

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