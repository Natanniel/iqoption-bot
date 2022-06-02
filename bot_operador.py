import sys
from threading import Timer
from time import sleep
from telegram.ext.updater import Updater # Conter a chave da api vinda do botfather
from src.dados import verificaUsuarioEmAlteracao,retornaTodosDadosDoUsuario
from iqoptionapi.stable_api import IQ_Option
import datetime
from datetime import timedelta

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
API.connect()
conexao = API.check_connect()

if conexao == False:
    ativo = False
    updater.bot.send_message(chat_id, 'Falha de Login IQOption.\n\nPor favor interrompa a operação e reconfigure sua conta IQOption')

while ativo:

    cliente,gerenciamento,gerenciamento_mao_fixa,lista = retornaTodosDadosDoUsuario(chat_id)
    #valida se ainda esta com alteração/operacao ativo
    ativo = verificaUsuarioEmAlteracao(chat_id)

    # Modalidades de operação
    operarMaoFixa = True
    
    # 
    proximaEntrada = []




    # Hora de pegar o proximo sinal com menos de 10 minutos para entrar
    horaAtual = datetime.datetime.now()

    for sinal in lista:
        dataHoraDoSinal = datetime.datetime.now()

        dataHoraDoSinal = datetime.datetime(year = dataHoraDoSinal.year, month= dataHoraDoSinal.month, day = dataHoraDoSinal.day , hour= int(sinal[4].split(":")[0]), minute= int(sinal[4].split(":")[1]) , second = int(sinal[4].split(":")[2])  )

        #2022-06-02 16:54:06.434271
     #   print(now.year, now.month, now.day, now.hour, now.minute, now.second)
        ## Coletando lista de sinais
        print(sinal)
        print(dataHoraDoSinal)
        # Subtract 2 minutes from datetime object
        final_time = dataHoraDoSinal - timedelta(minutes=60)
        print(final_time)
        print(horaAtual)
        
        sleep(100)






    