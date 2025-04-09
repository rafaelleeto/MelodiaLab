from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "chave_muito_segura"
import database

@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')

@app.route('/login') #rota para a página de login
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')


# VERFIFICAR O LOGIN
@app.route('/verificar-login', methods=['POST'])
def verificar_login():
# Pegando o que o usuário digitou no campo de entrada de user e senha
    username = request.form['username']
    password = request.form['password']

    # Verifica se o usuario digitado está na lista e se 
    # a senha está certa
    if username in usuarios and usuarios[username] == password:
        return redirect(url_for('home'))
    else:
        # Flash envia mensagem para o front-end
        flash('Usuário ou senha incorretos', 'danger')
        return redirect(url_for('login'))

@app.route('/cadastro',methods=['GET','POST'])
def cadastro():
    if request.method=='GET':
        return render_template('cadastro.html')
    email=request.form['email']
    nome=request.form['nome']
    senha=generate_password_hash(request.form['senha'])
    database.cadastro(email,nome,senha)
    return redirect('/login.html')

@app.route
    
    
    
    


# parte principal do
if __name__ == '__main__':
    app.run(debug=True)