import sys
from threading import Timer
from time import sleep
# Conter a chave da api vinda do botfather
from telegram.ext.updater import Updater
from src.dados import verificaUsuarioEmAlteracao, retornaTodosDadosDoUsuario
from iqoptionapi.stable_api import IQ_Option
import datetime
from datetime import timedelta

chat_id = 0
updater = Updater(
    "5389773517:AAEzhBQZ5vTExZ7MsA77OzTKhtbdgjoWctM", use_context=True)
#for parametro in sys.argv:
#    chat_id = parametro
chat_id = 782375549




cliente, gerenciamento, gerenciamento_mao_fixa, lista, martingale = retornaTodosDadosDoUsuario(
    chat_id)


real = 'REAL'
if gerenciamento[0][5] == False:
    real = 'PRACTICE'

# Valida conexão com IQOption
API = IQ_Option(gerenciamento[0][6], gerenciamento[0][7], real)
API.connect()
conexao = API.check_connect()

if conexao == False:
    ativo = False
    updater.bot.send_message(
        chat_id, 'Falha de Login IQOption.\n\nPor favor interrompa a operação e reconfigure sua conta IQOption')


## VARIAVEIS GLOBAIS ==================================
saldoInicial = API.get_balance() #Saldo inicial
saldoAtual = 0  # Saldo atual do usuario
lucro = 0 # Total perdido
loss = 0 # Total ganho
ativo = True  # Verifica se o processo ainda esta ativo
valorEntrada = 0 

quantidadeEntradas = 0 # Numero de entradas realizadas


def operarSinal(sinal):
    
    updater.bot.send_message(
        chat_id, 'Preparando entrada para o sinal \n ' + sinal[3] + ' ' + sinal[4] + ' ' + sinal[5])

    entrou = False
    perdeuSinal = False
    minuto = sinal[2]
    idEntrada = ''
    while entrou == False:
     
        dataHoraAtual = datetime.datetime.now()
        horaSinal = datetime.datetime(year=dataHoraAtual.year, month=dataHoraAtual.month, day=dataHoraAtual.day, hour=int(
            sinal[4].split(":")[0]), minute=int(sinal[4].split(":")[1]), second=int(sinal[4].split(":")[2]))
        delay = gerenciamento[0][1]
        sinalFinal = horaSinal - timedelta(seconds=delay + 1)
        passouMomentoSinal = horaSinal + timedelta(seconds=delay + 5)
        ativo = str(sinal[3].replace('/', ''))
        valorEntrada = float(gerenciamento_mao_fixa[0][2])
        acao = str(sinal[5])
        time = sinal[2]
        print(dataHoraAtual)
        print(sinalFinal)
        if dataHoraAtual > passouMomentoSinal:
            updater.bot.send_message(
                chat_id, 'Infelizmente o sinal foi perdido, provavelmente o sinal esta fechado inesperadamente. Sinta-se a vontade para comunicar o suporte em caso de falha')
            entrou = True
            perdeuSinal = True
        else:
            if dataHoraAtual >= sinalFinal:
                check, id = API.buy(valorEntrada, ativo, acao, time)
                if(check):
                    updater.bot.send_message(chat_id, 'Entrada realizada')
                    idEntrada = id    
                    entrou = True 
                else:
                    check, id = API.buy_digital_spot_v2(
                        ativo, valorEntrada, acao, time)
                    if(check):
                        updater.bot.send_message(chat_id, 'Entrada realizada')
                        idEntrada = id
                        entrou = True
                    else:
                        updater.bot.send_message(
                            chat_id, 'Falha ao realizar entrada, comunique o suporte imediatamente.')
   
    if perdeuSinal == False:
        resultado = API.check_win_v4(idEntrada)
     
        if(resultado[0] == 'win'):
            registraResultadoSinal(sinal, True, resultado[1], 0, idEntrada, 0, 0)
        else:
            tratarLoss(sinal, resultado, idEntrada, acao,time)

    else:
        registraResultadoSinal(sinal, False, 0, 0, 0, 0, 0)


def tratarLoss(sinal, resultado, idEntrada,acao,time):
    print(sinal)    
   
    registraResultadoSinal(sinal, False, 0, valorEntrada, 0, 0, 0)

    win = False
    martinGaleAtual = 1

    idEntrada = API.buy_digital_spot_v2(sinal[3].replace('/',''), gerenciamento_mao_fixa[0][2] * 2, acao, time)
  
    if(win == False and martingale[0][2] > martinGaleAtual):
        martinGaleAtual += 1
        updater.bot.send_message(chat_id, 'Verificando fator martingale')
        resultado = API.check_win_v4(idEntrada)
     
        if(resultado[0] == 'win'):
            registraResultadoSinal(sinal, True, resultado[1], 0, idEntrada, 0, 0)
            win = True
        else:
            tratarLoss(sinal, resultado, idEntrada, acao,time)

    


def registraResultadoSinal(sinal, status, win, loss, entrada, gales, soros):
    

    mensagem = 'Sinal realizado \n'
    if status == True:
        mensagem += 'Resultado : ✅ WIN \n'
        mensagem += 'Valor ganho : R$ ' + str(win) + '\n '

    if status == False:
        mensagem += 'Resultado : ❌ LOSS \n'
        mensagem += 'Valor perdido : R$ ' + str(loss) + '\n'

    updater.bot.send_message(chat_id, mensagem)

def verificaStopEMandaResumo():

    ativo = False


while ativo:

    cliente, gerenciamento, gerenciamento_mao_fixa, lista, martingale = retornaTodosDadosDoUsuario(
        chat_id)

    if(cliente[0][7] != 99):
        ativo = False

    if(len(lista)):

        # Modalidades de operação
        operarMaoFixa = True

        #
        proximaEntrada = []

        # Hora de pegar o proximo sinal com menos de 10 minutos para entrar
        horaAtual = datetime.datetime.now()

        for sinal in lista:
            dataHoraAtual = datetime.datetime.now()

            horaSinal = datetime.datetime(year=dataHoraAtual.year, month=dataHoraAtual.month, day=dataHoraAtual.day, hour=int(
                sinal[4].split(":")[0]), minute=int(sinal[4].split(":")[1]), second=int(sinal[4].split(":")[2]))

            sinalFinal = horaSinal + timedelta(minutes=1)
            if dataHoraAtual < sinalFinal:
                operarSinal(sinal)

        # valida se ainda esta com alteração/operacao ativo
        ativo = verificaUsuarioEmAlteracao(chat_id)

    else:
        updater.bot.send_message(chat_id, 'Lista de operacoes finalizadas')
        ativo = False
