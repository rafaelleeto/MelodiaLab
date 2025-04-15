import os
import hashlib
from flask import Flask, render_template, request, url_for, redirect, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import database

BUF_SIZE = 65536

UPLOAD_FOLDER = os.path.join("static","uploads")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.secret_key = "chave_muito_segura"


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    return redirect('/login')

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
    return redirect('/home')

@app.route('/home',methods=["GET"])
def home():
    musicas=database.pegar_musicas(session['email'])
    return render_template('home.html',musicas=musicas,session=session)

@app.route('/novo',methods=["GET","POST"])
def novo():
    if request.method=="GET":
        return render_template ('novo.html')
    file = request.files['imagem']
    
    if file and allowed_file(file.filename):
        sha256 = hashlib.sha256()
        while True:
            dados = file.stream.read(BUF_SIZE)
            if not dados:
                break
            sha256.update(dados)
        # filename = secure_filename(file.filename)
        file.stream.seek(0)
        filename = sha256.hexdigest()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    nome=request.form['nome']
    artista=request.form['artista']
    letra=request.form['letra']
    status=request.form['status']
    database.adicionar_musica(nome,artista,status,letra,session['email'],filename)
    return redirect('/home')
    
@app.route('/editar_musica/<int:id>',methods=["GET","POST"])
def editar(id):
    if request.method=="GET":
        if session['email']==database.pegar_musica(id)[5]:        
            musica=database.pegar_musica(id)
            return render_template('editar_musica.html',musica=musica)
        return "Você está tentando acessar a edição de uma musica que não é sua!"
    if session['email']==database.pegar_musica(id)[5]:
        nome=request.form['nome']
        artista=request.form['artista']
        letra=request.form['letra']
        status=request.form['status']
        database.atualizar_musica(nome,artista,status,letra,id)
        return redirect('/home')
    return "Você está tentando editar uma música que não é da sua conta"
    
@app.route('/excluir_musica/<id>',methods=["GET"])
def excluir_musica(id):
    if session['email']==database.pegar_musica(id)[5]:
        database.deletar_musica(id)
        return redirect('/home')
    return "Você está tentando deletar uma música que não é da sua conta"
    
        

@app.route("/excluir_conta",methods=["GET"])
def excluir_conta():
    email=session['email']
    database.excluir_conta(email)
    return redirect('/')

@app.route('/admin')
def admin():
    if session['email']=="leetobr@gmail.com":
        return render_template('admin.html')
    else:
        return "Você não tem permissão para entrar nessa página!"

@app.route('/admin/usuarios')
def usuario():
    if session['email']=="leetobr@gmail.com":
        usuarios=database.pegar_todos_usuarios()
        return render_template('usuarios.html',usuarios=usuarios)
    else:
        return "Você não tem permissão para entrar nessa página!"


@app.route('/admin/excluir_usuario/<email>')
def excluir_usuario_admin(email):
    if not email=="leetobr@gmail.com":
        database.excluir_conta(email)
    return redirect(url_for('usuario'))

@app.route('/admin/musicas')
def listar_musicas_admin():
    if session['email']=="leetobr@gmail.com":
        musicas=database.pegar_todas_musicas()
        return render_template('musicas.html',musicas=musicas)
    else:
        return "Você não tem permissão para entrar nessa página"
    
@app.route('/admin/excluir_musica/<id>')
def admin_excluir_musica(id):
    if session['email']=="leetobr@gmail.com":
        database.deletar_musica(id)
        return redirect(url_for('listar_musicas_admin'))
    else:
        return "Você não tem permissão para entrar nessa página"

if __name__ == '__main__':
    app.run(debug=True)