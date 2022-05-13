from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup 
from telegram.ext import CallbackQueryHandler
from telegram.ext.updater import Updater # Conter a chave da api vinda do botfather
from telegram.update import Update # Isso será invocado toda vez que um bot receber uma atualização
from telegram.ext.callbackcontext import CallbackContext # Não usaremos sua funcionalidade diretamente em nosso código, mas quando adicionarmos o dispatcher, será necessário (e funcionará internamente)
from telegram.ext.commandhandler import CommandHandler #Esta classe Handler é usada para lidar com qualquer comando enviado pelo usuário ao bot, um comando sempre começa com “/” ou seja, “/start”,”/help” etc.
from telegram.ext.messagehandler import MessageHandler #Esta classe Handler é usada para lidar com qualquer mensagem normal enviada pelo usuário ao bot
from telegram.ext.filters import Filters # Isso filtrará texto normal, comandos, imagens, etc. de uma mensagem enviada.
import re

from dados import retornaTodosDadosDoUsuario,verificarUsuarioTemChatLogado,VinculaContaAoChatID, configurarBaseDeDados,verificaEmailExisteBaseDeDados,entrarModoAlteracao,verificaUsuarioEmAlteracao


from menus.gerenciamento import entrarEmGerenciamento, alterarDelay,alterarStopWin,alterarStopLoss,alterarEmailIQ, alterarSenhaIQ,alterarModoReal
from menus.modooperacao import entrarEmModoOperacao
#from core.usuario import verificaEmailCadastrado

updater = Updater("5389773517:AAEzhBQZ5vTExZ7MsA77OzTKhtbdgjoWctM", use_context=True)



#   Processo do BOT
#   1 - Inicializar atravez do comando start
#   2 - Solicitar ao usuario o email cadastrado
#   3 - 

# inicializar o processo do BOT
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Informe abaixo o seu e-mail exatamente como você colocou quando foi realizar a sua inscrição em nosso produto :")
   
# Usuario informou o email
def validarEmail(update: Update, context: CallbackContext):
   

    if not re.match(r"[^@]+@[^@]+\.[^@]+",  update.message.text):
        update.message.reply_text("Formato de email invalido.")
    else: 

        existe = verificaEmailExisteBaseDeDados(update.message.chat_id, update.message.text)
        if(existe):
           
            VinculaContaAoChatID(update.message.chat_id, update.message.text)
            mainbutton = [
                ['🧠 Gerênciamento','⚙️ Modo de Operação'],
                ['🎯 Lista','🚨 Suporte'],
                ['🤖 Operar']
            ]
            keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
            message_reply_text = 'Seja muito bem vindo ! (Senhas em desenvolvimento)'
            update.message.reply_text(message_reply_text, reply_markup= keyBoard1)
        
        else:
            update.message.reply_text("O email informado não foi encontrado em nossa base de dados.")
            update.message.reply_text("Informe abaixo o seu e-mail exatamente como você colocou quando foi realizar a sua inscrição em nosso produto :")
    


def verificaComandosDeAlteracao(mensagem):
    alteracao = False

    if(mensagem == 'Alterar Gerenciamento' or mensagem == 'Conta IQOption'):
        alteracao = True
    
    return alteracao

def alteracao(update: Update, context: CallbackContext):
    
    cliente = retornaTodosDadosDoUsuario(update.message.chat_id)[0]
    
    # Gerenciamento
    if(cliente[0][7] == 1):
        if(cliente[0][8] == 1):
            alterarDelay(update,context)
        if(cliente[0][8] == 2):
            alterarStopWin(update,context)
        if(cliente[0][8] == 3):
            alterarStopLoss(update,context)
    
    if(cliente[0][7] == 2):
        if(cliente[0][8] == 1):
            alterarEmailIQ(update,context)
        if(cliente[0][8] == 2):
            alterarSenhaIQ(update,context)
        if(cliente[0][8] == 3):
            alterarModoReal(update,context)


def recepcionar(update: Update, context: CallbackContext):
    #configurarBaseDeDados()
    
    Logado = verificarUsuarioTemChatLogado(update.message.chat_id)
   
    # Verifica se o usuario ja esta logado nessa conversa
    if(Logado):

        #verifica se o usuario esta fazendo alguma alteração 
        if(verificaUsuarioEmAlteracao(update.message.chat_id)):
            alteracao(update, context)

        else:
            if(update.message.text == 'Voltar'):
                mainbutton = [
                    ['🧠 Gerênciamento','⚙️ Modo de Operação'],
                    ['🎯 Lista','🚨 Suporte'],
                    ['🤖 Operar']
                ]

                keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
                message_reply_text = 'Menu Principal'
                update.message.reply_text(message_reply_text, reply_markup= keyBoard1)

            else:       

                #Verificar se o que o usuario esta tentando fazer é alguma alteração
                if(verificaComandosDeAlteracao(update.message.text)):
                                    
                    if(update.message.text == 'Alterar Gerenciamento'):
                        entrarModoAlteracao(update.message.chat_id, 1, 1)
                        update.message.reply_text("Informe o valor de Delay para cada operação :")      

                    if(update.message.text == 'Conta IQOption'):
                        entrarModoAlteracao(update.message.chat_id, 2, 1)
                        update.message.reply_text("Informe seu email na IQOption :")      


                else:

                    if(update.message.text == '🧠 Gerênciamento'):
                        entrarEmGerenciamento(update,context)

                    else:
                        if(update.message.text == '⚙️ Modo de Operação'):
                            entrarEmModoOperacao(update,context)
                        else:
                            if not re.match(r"[^@]+@[^@]+\.[^@]+", update.message.text):
                                update.message.reply_text("Por favor informe um email válido")
                            else:
                                validarEmail(update,context)       

    else: 
        validarEmail(update,context)



updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, recepcionar))


updater.start_polling()
print('bot iniciado')
