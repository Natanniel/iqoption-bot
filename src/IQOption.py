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
    return order_id

def PegarStatusOperacao(IQ, id):
    return IQ.get_order(id)