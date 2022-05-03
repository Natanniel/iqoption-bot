from datetime import datetime
import time, json, sys, threading, requests, configparser, csv, os, colorama
from dateutil import tz
from colorama import Fore

def ClearScreen():
    sistema = os.name
    if sistema == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def timestamp_converter():
    hora = datetime.now()
    tm = tz.gettz('America/Recife')
    hora_atual = hora.astimezone(tm)
    return hora_atual.strftime('%H:%M:%S')

# Esta função coleta a lista de sinais e organiza de forma a operar os que ainda não foram operados
def LeituraListaDeSinais():
    global em_espera, get_profit 
    get_profit = True
    
    # Arquivo de simulação da lista
    arquivo = open('./lista.csv') 
    leitor = csv.reader(arquivo, delimiter=';')
    timeNow = timestamp_converter() 
    f = '%H:%M:%S' # Entender
    em_espera = [] 
  
    for row in leitor:
        if len(row[2]) == 5:
            horario = row[2] + ":00"
        else:
            horario = row[2]

        dif = int((  datetime.strptime(timeNow, f) - datetime.strptime(horario, f) ).total_seconds())
       

        # Filtro para excluir os sinais que ja se passaram os horarios
        if dif < 40:
            # Adiciona a diferença de tempo em segundos para posterior sorteio de menor valor
            row.append(dif)
            # Coloca os dados da paridade juntamente com o tempo restante para entrada em uma lista
            em_espera.append(row)
       
    # Verifica se a lista tem sinais pendentes para operar, caso contrario verifica se ainda tem posicoes abertas e aguarda o encerramento pra finalizar o bot
    if len(em_espera) == 0:
        print("Acabou")
      #  while True:
      #      thread_ativas = threading.active_count()
      #      if thread_ativas == 2:
      #          em_espera = False
      #          banca()
      #          mensagem = f'Lista de sinais finalizada..\nLucro: R${str(round(lucroTotal, 2))}\n'
      #          mensagem += f'Operações: {total_operacoes} | Vencedoras: {vitorias} | Perdedoras: {derrotas}\n Assertividade: {total_porcentagem}%\n'
      #          mensagem += f"Saldo da conta {'demo' if account_type == 'PRACTICE' else 'real'}: {account_balance}"
      #          print(f'{Fore.GREEN}{mensagem}')
      #          Mensagem(mensagem)
      #          sys.exit()
      #      else:
      #          print(
      #              f'{Fore.RED}AGUARDANDO FINALIZAÇÃO DE {Fore.GREEN}{thread_ativas - 2} THREADS', end='\x1b[K\r')
      #          time.sleep(60)
    
    else:
        # Ordena a lista pela entrada mais proxima
        em_espera.sort(key=lambda x: x[4], reverse=True)
        # Informa quantos sinais restam para serem executados
       # print(f'SINAIS PENDENTES: {len(em_espera)}')
        # Informa o próximo sinal a ser executado
       # print(f'{Fore.BLUE}PROXIMO: {em_espera[0][1]} | TEMPO: {em_espera[0][0]} | HORA: {em_espera[0][2]} | DIREÇÃO: {em_espera[0][3]}')
      
    return em_espera
      #  Mensagem(f'SINAIS PENDENTES: {len(em_espera)}\nPROXIMO: {em_espera[0][1]} | TEMPO: {em_espera[0][0]} | HORA: {em_espera[0][2]} | DIREÇÃO: {em_espera[0][3]}')



def banca():
    global account_type, account_balance, valor_da_banca
    account_type = config['conta']
    valor_da_banca = API.get_balance()
    account_balance = '${:,.2f}'.format(valor_da_banca) if API.get_currency(
    ) == 'USD' else 'R${:,.2f}'.format(valor_da_banca)
