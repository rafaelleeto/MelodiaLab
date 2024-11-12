from flask import Flask, render_template, request, url_for, redirect, flash
app = Flask(__name__)
app.secret_key = "chave_muito_segura"

# Cria uma lista e usuários e senha, depois vamos pegar no DB
usuarios = {
    'admin' : 'admin',
    'usuario' : 'senha',
    'rafaela' : '111111',
    'heitor' : '1271'
}

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

@app.route('/cadastro') #rota para a página de login
def cadastro():
    return render_template('cadastro.html')

# parte principal do
if __name__ == '__main__':
    app.run(debug=True)