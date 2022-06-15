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
        ['Voltar']
    ]
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    message_reply_text = '*⚙️PAINEL DE OPERAÇÂO*'
    update.message.reply_text(message_reply_text, reply_markup= keyBoard1, parse_mode='Markdown')



def entrarEmModoMaoFixa(update: Update, context: CallbackContext):   
    
    mainbutton = [
        ['Alterar mão fixa','Voltar p/ operações'],
        []
    ]   
    
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale = retornaTodosDadosDoUsuario(update.message.chat_id)

    if(len(gerenciamento_mao_fixa) == 0):
        comando = "INSERT INTO mao_fixa (cliente, valor_entrada )"
        comando += " VALUES ((select id from clientes where chat_id = '" + str(update.message.chat_id) + "'),0);"
        executarComando(comando)
        cliente,gerenciamento,gerenciamento_mao_fixa,lista = retornaTodosDadosDoUsuario(update.message.chat_id)

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
    
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale = retornaTodosDadosDoUsuario(update.message.chat_id)

    if(len(martingale) == 0):
        comando = "INSERT INTO martingale (cliente, niveis_gale )"
        comando += " VALUES ((select id from clientes where chat_id = '" + str(update.message.chat_id) + "'),0);"
        executarComando(comando)
        cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale = retornaTodosDadosDoUsuario(update.message.chat_id)

    mensagem = '*⚙️PAINEL DE OPERAÇÂO* - ___🔂 Martin-Gale___\n\n'
    mensagem += 'Consiste em apostar repetidamente e progressivamente na mesma equipe/mercado no caso de derrota, até ela ganhar. O objetivo consiste em recuperar o que terá perdido, e lucrar quando ganhar.\n\n'
    mensagem += 'Manter o fator em 0 configura ele como desativado\n'
    mensagem += '*Niveis de Martin-gale* : ' + str(martingale[0][1]) + '\n'
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    update.message.reply_text(mensagem, reply_markup= keyBoard1, parse_mode='Markdown')
  