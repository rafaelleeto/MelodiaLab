from flask import Flask, render_template, request, url_for, redirect, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "chave_muito_segura"
import database

@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')

@app.route('/cadastro',methods=['GET','POST'])
def cadastro():
    if request.method=='GET':
        return render_template('cadastro.html')
    email=request.form['email']
    verificação=database.verificar_se_usuario_existe(email)
    if verificação:
        return "Você não pode cadastrar um email que já esta em uso"
    senha=request.form['senha']
    nome=request.form['nome']
    senha=generate_password_hash(request.form['senha'])
    database.cadastro(email,nome,senha)
    return redirect(url_for('login'))

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template('login.html')
    email=request.form['email']
    verificação=database.verificar_se_usuario_existe(email)
    if not verificação:
        return "Algo deu de errado, tente novamente"
    senha=request.form['senha']
    listadobanco=database.pegar_senha(email)
    if not check_password_hash(listadobanco[0],senha):
        return 'pode nao'
    session['email']=request.form['email']
    return redirect(url_for('home'))

@app.route('/home',methods=["GET"])
def home():
    musicas=database.pegar_musicas(session['email'])
    return render_template('home.html',musicas=musicas)

@app.route('/novo',methods=["GET","POST"])
def novo():
    if request.method=="GET":
        return render_template ('novo.html',)
    nome=request.form['nome']
    artista=request.form['artista']
    letra=request.form['letra']
    status=request.form['status']
    database.adicionar_musica(nome,artista,status,letra,session['email'])
    return redirect(url_for('home'))
    

    
   
    












if __name__ == '__main__':
    app.run(debug=True)