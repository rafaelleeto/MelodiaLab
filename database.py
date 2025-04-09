import sqlite3

def conectar_banco():
    conexao=sqlite3.connect("musica.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (email TEXT PRIMARY KEY,nome TEXT , senha TEXT )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS musicas (id INTEGER PRIMARY KEY, artista TEXT,letra TEXT, 
                   email_usuario text, FOREIGN KEY (email_usuario) REFERENCES usuario(email))''')
    conexao.commit()
    cursor.close()

def cadastro(email,nome,senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO usuarios (email,nome,senha) VALUES (?,?,?)''',(email,nome,senha))
    conexao.commit()
    cursor.close()
    
    
if __name__=="__main__":
    criar_tabelas()