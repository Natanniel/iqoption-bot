import sqlite3

def configurarBaseDeDados():
   con = sqlite3.connect("database.db")
   cur = con.cursor()
   comando = "CREATE TABLE clientes ("
   comando += " id               INTEGER      PRIMARY KEY AUTOINCREMENT,"
   comando += " email            STRING (200),"
   comando += " senha            STRING (32),"
   comando += " status           BOOLEAN,"
   comando += " chat_id          STRING (64),"
   comando += " usuario_iqoption STRING (200),"
   comando += " senha_iqoption   STRING (64)) "
  
  
   #cur.execute(comando)
   comando = "INSERT INTO clientes (email,senha,status,chat_id,usuario_iqoption,senha_iqoption)"
   comando += "VALUES ('natanniel.alves@outlook.com','123456',1,null,'','')"
   #cur.execute(comando)
   
   comando = "CREATE TABLE gerenciamento ( "
   comando += "   id        INTEGER PRIMARY KEY AUTOINCREMENT, "
   comando += "   delay     INTEGER, "
   comando += "   stop_win  INTEGER, "
   comando += "   stop_loss INTEGER, "
   comando += "   cliente   INTEGER REFERENCES clientes (id)  "
   comando += "); "
   #cur.execute(comando)

   con.commit()
   con.close()
   


# Verifica se o usuario existe algum chat iniciado
def verificarUsuarioTemChatLogado(chatID):
   con = sqlite3.connect('database.db')
   cur = con.cursor()
   existe = False
   for row in cur.execute("SELECT * FROM clientes where chat_id = '"+ str(chatID)+"' "):
      existe = True
   con.close()
   return existe

def verificaEmailExisteBaseDeDados(chatID, email):
   con = sqlite3.connect('database.db')
   cur = con.cursor()
   existe = False
   for row in cur.execute("SELECT * FROM clientes where email = '"+ email +"' "):
      existe = True
 #     cur.execute("update clientes set chat_id = '" + str(chatID) +"' where email = '" + email +"' ")
   con.close()
   return existe

def VinculaContaAoChatID(chatID, email):
   con = sqlite3.connect("database.db")
   cur = con.cursor()
  
   comando = "update clientes set chat_id = '"+ str(chatID)+"' where email = '"+email+"'"
   cur.execute(comando)
   con.commit()
   con.close()

def retornaTodosDadosDoUsuario(chatID):
       
   con = sqlite3.connect("database.db")
   cur = con.cursor()

   cliente = []
   gerenciamento = []
   gerenciamento_mao_fixa = []
   
   for row in cur.execute("SELECT * FROM clientes where chat_id = '"+ str(chatID)+"' "):
      cliente.append(row)
      for row2 in cur.execute("SELECT * FROM gerenciamento where cliente = "+ str(row[0])+" "):
         gerenciamento.append(row2)
      for row2 in cur.execute("SELECT * FROM mao_fixa where cliente = "+ str(row[0])+" "):
         gerenciamento_mao_fixa.append(row2)

   con.commit()
   con.close()
   return cliente,gerenciamento,gerenciamento_mao_fixa

def entrarModoAlteracao(chatID, modo_alteracao, modo_alteracao_passo):
   con = sqlite3.connect("database.db")
   cur = con.cursor()
  
   comando = "update clientes set modo_alteracao = "+ str(modo_alteracao)+",modo_alteracao_passo = "+ str(modo_alteracao_passo)+"  where chat_id = '"+ str(chatID)+"'"
   cur.execute(comando)
   con.commit()
   con.close()

def verificaUsuarioEmAlteracao(chatID):
   emAlteracao = False
   con = sqlite3.connect("database.db")
   cur = con.cursor()
   for row in cur.execute("SELECT * FROM clientes where chat_id = '"+ str(chatID)+"' and modo_alteracao != 0"):
      emAlteracao = True
         
   return emAlteracao

def executarComando(comando):
   con = sqlite3.connect("database.db")
   cur = con.cursor()
   cur.execute(comando)
   con.commit()
   con.close()