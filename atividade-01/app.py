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
@app.route('/lista')
def lista():
    return render_template('lista.html')
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')


#iniciando o servidor na porta 5000
if __name__ == '__main__':
# if esta verificando se o arquivo gravado em __name__ é o arquivo prinicipal
    app.run(port=5000, debug=True)
# o metodo .run() inicia o servidor
