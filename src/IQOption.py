from iqoptionapi.stable_api import IQ_Option
from src.Helper import ClearScreen

# Autenticação na IQOption
def IQLogin(email,senha):

    print("Conectando ...")
    api = IQ_Option(email,senha)
    status, reason = api.connect()
    
    if status == True:
        api.change_balance("PRACTICE")
        #MODE: "PRACTICE"/"REAL"
        return api

def ObterValorBanca(api):
    return api.get_balance()

def Operar(IQ, ativo, valor, acao, tempo):
    print(ativo)
    print(valor)
    print(acao)
    print(tempo)
    status, order_id = IQ.buy_digital_spot_v2(ativo, valor, acao, tempo)

    print(status)
    print(IQ.check_win_digital_v2(buy_order_id = order_id))
    return order_id

def PegarStatusOperacao(IQ, id):
    print(IQ.get_position_history_v2(id, polling_time=1))
    print('1 2 3')
    return IQ.check_win_digital(id, polling_time=1)


    

    
    