from flask import Flask, render_template
from controllers import routes
#carregando o Flask na variavel "app"
#declarando variavel no python
app = Flask(__name__, template_folder='views')
#variaveis com __ são variaveis de ambiente do python
#__name__ representa o nome da aplicação
routes.init_app(app)





#iniciando o servidor na porta 5000
if __name__ == '__main__':
# if esta verificando se o arquivo gravado em __name__ é o arquivo prinicipal
    app.run(port=5000, debug=True)
# o metodo .run() inicia o servidor
