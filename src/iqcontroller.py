from src.dados import retornaTodosDadosDoUsuario
#from interface_telegram.ioption.iqoptionapi.stable_api import IQ_Option
from iqoptionapi.stable_api import IQ_Option

def verificarSaldo(chat_id):
    saldo = 0
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(chat_id)    
    
    iqoptionConfigurado = False
    
    for row in gerenciamento:
      
        acType = "PRACTICE"
        if row[5] == 1 :
          acType =  "REAL"

        API = IQ_Option(row[6], row[7], active_account_type= acType )
        
        API.connect()
        iqoptionConfigurado = API.check_connect()

        if(iqoptionConfigurado):
          saldo = API.get_balance()

          # saldo


    return saldo,iqoptionConfigurado