from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from telegram.ext.updater import Updater # Conter a chave da api vinda do botfather
from telegram.update import Update # Isso será invocado toda vez que um bot receber uma atualização
from telegram.ext.callbackcontext import CallbackContext # Não usaremos sua funcionalidade diretamente em nosso código, mas quando adicionarmos o dispatcher, será necessário (e funcionará internamente)
from telegram.ext.commandhandler import CommandHandler #Esta classe Handler é usada para lidar com qualquer comando enviado pelo usuário ao bot, um comando sempre começa com “/” ou seja, “/start”,”/help” etc.
from telegram.ext.messagehandler import MessageHandler #Esta classe Handler é usada para lidar com qualquer mensagem normal enviada pelo usuário ao bot
from telegram.ext.filters import Filters # Isso filtrará texto normal, comandos, imagens, etc. de uma mensagem enviada.
from src.dados import executarComando, retornaTodosDadosDoUsuario

def entrarEmLista(update: Update, context: CallbackContext):
   
    mainbutton = [
        ['✅ Adicionar Sinais','❌ Limpar Lista'],
        ['Voltar']
    ]
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    mensagem = 'Lista de Sinais \n\n'
    
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(update.message.chat_id)

    if(len(lista) > 0):
        for sinal in lista:
            mensagem += str(sinal[4]) +' ' + str(sinal[3]) +' ' + str(sinal[5]) +' ' + str(sinal[2]) + '\n'
    else: 
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
            update.message.reply_text("O Bot não entendeu o seu comando.\nDigite um caracter válido :")
    except:
        update.message.reply_text("O Bot não entendeu o seu comando.\nDigite um caracter válido :")

def adicionarLista(update: Update, context: CallbackContext):
      
    try:        
        sinais = update.message.text.split('\n')
            
        for sinal in sinais:
          #  update.message.reply_text(sinal)
            x = sinal.split(';')

            hora = str(x[0]) + ':00'
            par = str(x[1])
            minuto = str(x[3])
            sinal = str(x[2])
            
            
            executarComando("insert into lista (cliente,minuto,par,horario,sinal) values ((select id from clientes where chat_id = '"+str(update.message.chat_id)+"'), "+ minuto+", '"+ par+"', '"+hora+"', '"+sinal+"'   )")


        executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
        update.message.reply_text("Lista inserida com sucesso !")
        entrarEmLista(update,context)
       
    except:
        update.message.reply_text("Não entendi.\nVerifique o formato da sua lista e tente novamente :")
