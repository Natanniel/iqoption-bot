import time, json, sys, threading, requests, configparser, csv, os, colorama
from tokenize import Double
from src.IQOption import IQLogin, ObterValorBanca, Operar,PegarStatusOperacao
from src.Helper import ClearScreen,LeituraListaDeSinais,timestamp_converter


ContaIQ = 'null' # sessão autenticada na IQOption
global banca
ciclo = 0

def configuracao():
    global vitorias, derrotas, total_operacoes, total_porcentagem
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')
  
   # return {'entrada': arquivo.get('GERAL', 'entrada'), 'entrada_percentual': arquivo.get('GERAL', 'entrada_percentual'), 'conta': arquivo.get('GERAL', 'conta'), 'stop_win': arquivo.get('GERAL', 'stop_win'), 'stop_loss': arquivo.get('GERAL', 'stop_loss'), 'payout': 0, 'banca_inicial': 0, 'martingale': arquivo.get('GERAL', 'martingale'), 'mgProxSinal': arquivo.get('GERAL', 'mgProxSinal'), 'valorGale': arquivo.get('GERAL', 'valorGale'), 'niveis': arquivo.get('GERAL', 'niveis'), 'analisarTendencia': arquivo.get('GERAL', 'analisarTendencia'), 'noticias': arquivo.get('GERAL', 'noticias'), 'timerzone': arquivo.get('GERAL', 'timerzone'), 'hitVela': arquivo.get('GERAL', 'hitVela'), 'telegram_token': arquivo.get('telegram', 'telegram_token'), 'telegram_id': arquivo.get('telegram', 'telegram_id'), 'usar_bot': arquivo.get('telegram', 'usar_bot'), 'email': arquivo.get('CONTA', 'email'), 'senha': arquivo.get('CONTA', 'senha'), 'trailing_stop': arquivo.get('GERAL', 'trailing_stop'), 'trailing_stop_valor': arquivo.get('GERAL', 'trailing_stop_valor'), 'payout_minimo': arquivo.get('GERAL', 'payout'), 'usar_ciclos': arquivo.get('CICLOS', 'usar_ciclos'), 'ciclos_nivel': arquivo.get('CICLOS', 'nivel_ciclos')}
    return {
        'email': arquivo.get('CONTA', 'email'), 
        'senha': arquivo.get('CONTA', 'senha'),

        'soros' : arquivo.get('SOROS', 'ativo'),
        'soros-tipo' : arquivo.get('SOROS', 'tipo'),
        'soros-nivel' : arquivo.get('SOROS', 'nivel'),
        'soros-entrada' : arquivo.get('SOROS', 'entrada'),
     
    }

config = configuracao()
ContaIQ = IQLogin(config['email'], config['senha'])


if(ContaIQ.check_connect() == True):
    ClearScreen()
    print("Conectado com saldo de :", ContaIQ.get_balance())
    banca = ObterValorBanca(ContaIQ)
    
    

    # Iniciando Atividade do BOT
    while True:

        lista = LeituraListaDeSinais()
        soro_ganhos = 0  # valor do ultimo ganho na operação soro      

        if len(lista) > 0:
           
            # acompanhar oportunidade pelo console log
            ClearScreen()
            print('Esperando proxima oportunidade') 
            time.sleep(1)

            #status = PegarStatusOperacao(ContaIQ,order_id)
            #print(status)

            # Chegado o momento da operação
            if(lista[0][2] == (str(timestamp_converter()).split(':')[0] + ':' +  str(timestamp_converter()).split(':')[1] )):
            #if True:                
                # Verifica modalidade de operação Soros
                if config['soros'] == "S":

                    # SOROS conservador ele reinicia a alavancagem na perda
                    if config['soros-tipo'] == 'Conservador':
                        
                        # Realiza a operação Soro   
                        order_id = Operar(
                            ContaIQ, #Variavel com a autenticação da IQ
                            lista[0][1], # Pegando a moeda
                            (float(config['soros-entrada']) + soro_ganhos), # Calculo do valor fixo soros + o ultimo ganho
                            lista[0][3], # Tipo de operação compra ou venda
                            int(str(lista[0][0]).replace('M','')) # Tempo de gráfico
                        )
                        
                        print('Realizou a operação e agora é necessário aguardar')
                        time.sleep(int(str(lista[0][0]).replace('M','')) * 60 )
                        status = PegarStatusOperacao(ContaIQ,order_id)

                        # Se perdeu a operação irá zerar os soros e tambem o ciclo
                        if(status[0] == False) :
                            soro_ganhos = 0
                            ciclo = 0
                            time.sleep(5)
                            print('Perdeu')
                                
                        # Ganhar irá aumentar a contagem do ciclo ou zerar caso tenha chegado ao limite de Soros
                        else:
                            print(status)
                            print('ganhou')                            
                            ciclo += 1
                            soro_ganhos = 0.80
                            time.sleep(60)


                    # SOROS Agressivo ele nao reicinia a alavancagem na perda
                    if config['soros-tipo'] == 'Agressivo':
                        
                        # Realiza a operação Soro   
                        order_id = Operar(
                            ContaIQ, #Variavel com a autenticação da IQ
                            lista[0][1], # Pegando a moeda
                            (float(config['soros-entrada']) + soro_ganhos), # Calculo do valor fixo soros + o ultimo ganho
                            lista[0][3], # Tipo de operação compra ou venda
                            int(str(lista[0][0]).replace('M','')) # Tempo de gráfico
                        )
                        
                        print('Realizou a operação e agora é necessário aguardar')
                        time.sleep(int(str(lista[0][0]).replace('M','')) * 60 )
                        status = PegarStatusOperacao(ContaIQ,order_id)
                                
                        print(status)
                        ciclo += 1
                        soro_ganhos = 0.80
                        time.sleep(60)


                    # Verifica se é necessario resetar o ciclo do soro
                    if(ciclo <= int(config['soros-nivel'])): 
                        ciclo = 0
                        soro_ganhos = 0

                    # SOROS agressivo conserva o aumento da aposta
                # if config['soros-tipo'] == 'Agressivo':

                # print(lista)
                

            


            









