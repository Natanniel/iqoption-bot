from src.dados import retornaTodosDadosDoUsuario
#from interface_telegram.ioption.iqoptionapi.stable_api import IQ_Option

def verificarSaldo(chat_id):
    saldo = 0
    cliente,gerenciamento,gerenciamento_mao_fixa,lista = retornaTodosDadosDoUsuario(chat_id)    
    
    iqoptionConfigurado = False
    
    for row in gerenciamento:
        print('Tem algo em gerenciamento')

      #  API = IQ_Option(row[5], row[6])


    return saldo,iqoptionConfigurado