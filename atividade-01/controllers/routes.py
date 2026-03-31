from flask import render_template, request, redirect, url_for

usuarios = [{"nome" : "caio" , "email" : "caio@g" , "senha" : "123"}]

produtos = []

def init_app(app):

    @app.route("/", methods=["GET", "POST"])
    def home():
        return render_template("index.html")
    
    @app.route("/lista", methods=["GET", "POST"])
    def lista():
        if request.method == "POST":
            produtos.append({
                "nome_produto": request.form.get("nome_produto"),
                "categoria": request.form.get("categoria"),
                "preco": request.form.get("preco")
            })
            return redirect (url_for('lista'))

        return render_template("lista.html", produtos=produtos)

    @app.route("/formulario", methods=["GET","POST"])
    def formulario():
        if request.method == "POST":
            


            usuarios.append({
                "nome": request.form.get("nome"),
                "email": request.form.get("email"),
                "senha": request.form.get("senha")
            })

        return render_template("formulario.html", usuarios=usuarios)
    
  