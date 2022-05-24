import sys
from telegram.ext.updater import Updater # Conter a chave da api vinda do botfather
from src.dados import verificaUsuarioEmAlteracao,retornaTodosDadosDoUsuario
from iqoptionapi.stable_api import IQ_Option

chat_id = 0
updater = Updater("5389773517:AAEzhBQZ5vTExZ7MsA77OzTKhtbdgjoWctM", use_context=True)
#for parametro in sys.argv:
#    chat_id = parametro

# TESTE
chat_id = 782375549

ativo = True


cliente,gerenciamento,gerenciamento_mao_fixa,lista = retornaTodosDadosDoUsuario(chat_id)


# Valida conexão com IQOption
API = IQ_Option(cliente[0][1], cliente[0][2])
conexao = API.check_connect()

if conexao == False:
    ativo = False
    updater.bot.send_message(chat_id, 'O BOT não conseguiu fazer login na IQOption. Por favor interrompa a operação e configure sua conta IQOPtion')

while ativo:

    


    



    #valida se ainda esta com alteração/operacao ativo
    ativo = verificaUsuarioEmAlteracao(chat_id)



    