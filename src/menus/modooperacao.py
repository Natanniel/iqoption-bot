from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from telegram.ext.updater import Updater # Conter a chave da api vinda do botfather
from telegram.update import Update # Isso será invocado toda vez que um bot receber uma atualização
from telegram.ext.callbackcontext import CallbackContext # Não usaremos sua funcionalidade diretamente em nosso código, mas quando adicionarmos o dispatcher, será necessário (e funcionará internamente)
from telegram.ext.commandhandler import CommandHandler #Esta classe Handler é usada para lidar com qualquer comando enviado pelo usuário ao bot, um comando sempre começa com “/” ou seja, “/start”,”/help” etc.
from telegram.ext.messagehandler import MessageHandler #Esta classe Handler é usada para lidar com qualquer mensagem normal enviada pelo usuário ao bot
from telegram.ext.filters import Filters # Isso filtrará texto normal, comandos, imagens, etc. de uma mensagem enviada.
from src.dados import executarComando, retornaTodosDadosDoUsuario

def entrarEmModoOperacao(update: Update, context: CallbackContext):
   
    banca = 0
    delay = 2
    stop_win = 0
    stop_loss = 0

    mainbutton = [
        ['🖐️ Mão Fixa','🔂 Margin-Gale'],
        ['↗️ Soros','Voltar']
    ]
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    message_reply_text = '*⚙️PAINEL DE OPERAÇÂO*'
    update.message.reply_text(message_reply_text, reply_markup= keyBoard1, parse_mode='Markdown')



def entrarEmModoMaoFixa(update: Update, context: CallbackContext):   
    
    mainbutton = [
        ['Alterar mão fixa','Voltar p/ operações'],
        []
    ]   
    
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(update.message.chat_id)

    if(len(gerenciamento_mao_fixa) == 0):
        comando = "INSERT INTO mao_fixa (cliente, valor_entrada )"
        comando += " VALUES ((select id from clientes where chat_id = '" + str(update.message.chat_id) + "'),0);"
        executarComando(comando)
        cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(update.message.chat_id)

    mensagem = '*⚙️PAINEL DE OPERAÇÂO* - ___🖐️ Mão Fixa___\n\n'
    mensagem += 'A mão fixa mantem um ciclo de apostas fixas ate que os sinais da lista seja cumprida ou a meta diaria seja atingida (Win/Loss).\n\n'
    mensagem += '*💰 Valor das entradas* : R$ ' + str(gerenciamento_mao_fixa[0][2]) + '\n'
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    update.message.reply_text(mensagem, reply_markup= keyBoard1, parse_mode='Markdown')
  
  
def alterarMaoFixa(update: Update, context: CallbackContext):
  
    try:        
        executarComando("update mao_fixa set valor_entrada = "+ str(update.message.text) + " where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
        executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
        update.message.reply_text("Mão fixa atualizado com sucesso !")
        entrarEmModoMaoFixa(update,context)      
    except:
        update.message.reply_text("Falha ao alterar entrada.\n digite um numero válido :")


def entrarEmModoMartinGale(update: Update, context: CallbackContext):   
    
    mainbutton = [
        ['Alterar Martin-gale','Voltar p/ operações'],
        []
    ]   
    
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(update.message.chat_id)

    if(len(martingale) == 0):
        comando = "INSERT INTO martingale (cliente, niveis_gale )"
        comando += " VALUES ((select id from clientes where chat_id = '" + str(update.message.chat_id) + "'),0);"
        executarComando(comando)
        cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(update.message.chat_id)

    mensagem = '*⚙️PAINEL DE OPERAÇÂO* - ___🔂 Martin-Gale___\n\n'
    mensagem += 'Consiste em apostar repetidamente e progressivamente na mesma equipe/mercado no caso de derrota, até ela ganhar. O objetivo consiste em recuperar o que terá perdido, e lucrar quando ganhar.\n\n'
    mensagem += '___Manter o fator em 0 configura ele como desativado___\n'
    mensagem += '*Niveis de Martin-gale* : ' + str(martingale[0][2]) + '\n'
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    update.message.reply_text(mensagem, reply_markup= keyBoard1, parse_mode='Markdown')
  
def alterarMartinGale(update: Update, context: CallbackContext):
      
    try:        
        executarComando("update martingale set niveis_gale = "+ str(update.message.text) + " where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
        executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
        update.message.reply_text("Martin-Gale atualizado com sucesso !")
        entrarEmModoMartinGale(update,context)      
    except:
        update.message.reply_text("Falha ao alterar entrada.\n digite um numero válido :")



def entrarEmModoSoros(update: Update, context: CallbackContext):

   
    mainbutton = [
        ['Alterar Soros','Voltar p/ operações']
      
    ]   
    
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(update.message.chat_id)

    if(len(soros) == 0):
        comando = "INSERT INTO soros (cliente )"
        comando += " VALUES ((select id from clientes where chat_id = '" + str(update.message.chat_id) + "'));"
        executarComando(comando)
        cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(update.message.chat_id)

    mensagem = '*⚙️PAINEL DE OPERAÇÂO* - ___↗️ Soros___\n\n'
    mensagem += 'O gerenciamento de soros consiste em buscar sequências de vitórias, sempre reinvestindo o valor total/metade dos ganhos de operações anteriores. \n\n'
    mensagem += '___Manter o fator em 0 configura ele como desativado___\n'
    mensagem += '*Niveis de Soros* : ' + str(soros[0][2]) + '\n'
    mensagem += '*Porcentagem de Soros* : ' + str(soros[0][3]) + '\n'
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    update.message.reply_text(mensagem, reply_markup= keyBoard1, parse_mode='Markdown')

def alterarSoros(update: Update, context: CallbackContext):
      
    try:        
        executarComando("update soros set niveis = "+ str(update.message.text) + " where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
        executarComando("update clientes set modo_alteracao_passo = 4 where chat_id = '" + str(update.message.chat_id) + "'")
        update.message.reply_text("Informe o percentual para o fator Soros : ")
    except:
        update.message.reply_text("Falha ao alterar entrada.\n digite um numero válido :")



def alterarSorosPorcentagem(update: Update, context: CallbackContext):
      
    try:        
        executarComando("update soros set percentual = "+ str(update.message.text) + " where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
        executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
        update.message.reply_text("Soros atualizado com sucesso !")
        entrarEmModoSoros(update,context)      
    except:
        update.message.reply_text("Falha ao alterar entrada.\n digite um numero válido :")


