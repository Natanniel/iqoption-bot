from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from telegram.ext.updater import Updater # Conter a chave da api vinda do botfather
from telegram.update import Update # Isso será invocado toda vez que um bot receber uma atualização
from telegram.ext.callbackcontext import CallbackContext # Não usaremos sua funcionalidade diretamente em nosso código, mas quando adicionarmos o dispatcher, será necessário (e funcionará internamente)
from telegram.ext.commandhandler import CommandHandler #Esta classe Handler é usada para lidar com qualquer comando enviado pelo usuário ao bot, um comando sempre começa com “/” ou seja, “/start”,”/help” etc.
from telegram.ext.messagehandler import MessageHandler #Esta classe Handler é usada para lidar com qualquer mensagem normal enviada pelo usuário ao bot
from telegram.ext.filters import Filters # Isso filtrará texto normal, comandos, imagens, etc. de uma mensagem enviada.
from dados import executarComando, retornaTodosDadosDoUsuario

def entrarEmLista(update: Update, context: CallbackContext):
   
    mainbutton = [
        ['✅ Adicionar Sinais','❌ Limpar Lista'],
        ['Voltar']
    ]
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    mensagem = 'Lista de Sinais \n\n'
    mensagem += 'Nenhum sinal cadastrado'
    update.message.reply_text(mensagem, reply_markup= keyBoard1)



  
def limparLista(update: Update, context: CallbackContext):
  
    try:        
        if(update.message.text == 'S' or update.message.text == 'N'):
            if(update.message.text == 'S'):
                executarComando("delete from lista where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
                executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
                update.message.reply_text("Lista excluida com sucesso !")
            else:
                executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
                update.message.reply_text("Sua lista não foi excluida.")
            
            entrarEmLista(update,context) 
        else:
            update.message.reply_text("O Bot nao entendeu o seu comando.\nDigite um caracter válido :")
    except:
        update.message.reply_text("O Bot nao entendeu o seu comando.\nDigite um caracter válido :")

def adicionarLista(update: Update, context: CallbackContext):
      
    try:        
        if(update.message.text == 'S' or update.message.text == 'N'):
            if(update.message.text == 'S'):
                executarComando("delete from lista where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
                executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
                update.message.reply_text("Lista excluida com sucesso !")
            else:
                executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
                update.message.reply_text("Sua lista não foi excluida.")
            
            entrarEmLista(update,context) 
        else:
            update.message.reply_text("O Bot nao entendeu o seu comando.\nDigite um caracter válido :")
    except:
        update.message.reply_text("O Bot nao entendeu o seu comando.\nDigite um caracter válido :")
