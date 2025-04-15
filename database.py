import sqlite3

def conectar_banco():
    conexao=sqlite3.connect("musica.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (email TEXT PRIMARY KEY,nome TEXT , senha TEXT )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS musicas (id INTEGER PRIMARY KEY,nome TEXT, artista TEXT, status TEXT,
                   letra TEXT, email_usuario TEXT, capa TEXT,  FOREIGN KEY (email_usuario) REFERENCES usuario(email))''')
    conexao.commit()
    cursor.close()

def cadastro(email,nome,senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO usuarios (email,nome,senha) VALUES (?,?,?)''',(email,nome,senha))
    conexao.commit()
    cursor.close()

def pegar_senha(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' SELECT senha FROM usuarios WHERE email=?''',(email,))
    conexao.commit()
    return cursor.fetchone()

def verificar_se_usuario_existe(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM usuarios WHERE email=?''',(email,))
    conexao.commit()
    return cursor.fetchone()

def adicionar_musica(nome,artista,status,letra,email,filename):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    if nome=="1" and artista=="1" and status=="1" and letra=="1":
        return "pode nao"
    cursor.execute('''INSERT INTO musicas (nome,artista,status,letra,email_usuario,capa) VALUES(?,?,?,?,?,?)''',(nome,artista,status,letra,email,filename))
    conexao.commit()
    cursor.close()

def pegar_musicas(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM musicas WHERE email_usuario=?''',(email,))
    conexao.commit()
    return cursor.fetchall()
    
def pegar_musica(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM musicas WHERE id=?''',(id,))
    conexao.commit()
    return cursor.fetchone()


def atualizar_musica(nome,artista,status,letra,id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    print(id)
    cursor.execute('''UPDATE musicas SET nome=? , artista=? , status=?, letra=? WHERE id=? ''',(nome,artista,status,letra,id))
    conexao.commit()
    cursor.close()

def deletar_musica(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''DELETE FROM musicas WHERE id=? ''',(id,))
    conexao.commit()
    cursor.close()
    
def excluir_conta(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''DELETE FROM musicas WHERE email_usuario=? ''',(email,))
    cursor.execute('''DELETE FROM usuarios WHERE email=? ''',(email,))
    conexao.commit()
    cursor.close()
    
def pegar_todos_usuarios():
    conexao = conectar_banco()
    conexao.row_factory=sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM usuarios ''')
    conexao.commit()
    return cursor.fetchall()

def pegar_todas_musicas():
    conexao = conectar_banco()
    conexao.row_factory=sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM musicas ''')
    conexao.commit()
    return cursor.fetchall()




    
if __name__=="__main__":
    criar_tabelas()