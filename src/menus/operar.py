import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from telegram.ext.updater import Updater # Conter a chave da api vinda do botfather
from telegram.update import Update # Isso será invocado toda vez que um bot receber uma atualização
from telegram.ext.callbackcontext import CallbackContext # Não usaremos sua funcionalidade diretamente em nosso código, mas quando adicionarmos o dispatcher, será necessário (e funcionará internamente)
from telegram.ext.commandhandler import CommandHandler #Esta classe Handler é usada para lidar com qualquer comando enviado pelo usuário ao bot, um comando sempre começa com “/” ou seja, “/start”,”/help” etc.
from telegram.ext.messagehandler import MessageHandler #Esta classe Handler é usada para lidar com qualquer mensagem normal enviada pelo usuário ao bot
from telegram.ext.filters import Filters # Isso filtrará texto normal, comandos, imagens, etc. de uma mensagem enviada.
from src.dados import executarComando, retornaTodosDadosDoUsuario
from src.menus.gerenciamento import entrarEmGerenciamento

def entrarEmOperar(update: Update, context: CallbackContext):
   
    mainbutton = [
        ['🤖🖐️ Mão Fixa','Margin-Gale'],
        ['Voltar']
    ]
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    mensagem = 'OPERAR \n\n'
    mensagem += 'Por favor, selecione a modalidade de operação que deseja iniciar o seu robô.'

   
    update.message.reply_text(mensagem, reply_markup= keyBoard1)


def entrarEmOperarMaoFixa(update: Update, context: CallbackContext):
       
    mainbutton = [
        ['🤖✅ Confirmar','🤖❌ Cancelar']
    ]
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    mensagem = 'OPERAR MÂO FIXA \n\n'
    update.message.reply_text(mensagem, reply_markup= keyBoard1)
   
    executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 20 where chat_id = '" + str(update.message.chat_id) + "'")
    
   
def cancelarOperacao(update: Update, context: CallbackContext):
    executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
    entrarEmOperar(update,context)

    
def confirmarOperacao(update: Update, context: CallbackContext):
    executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 99 where chat_id = '" + str(update.message.chat_id) + "'")
    
    os.system('python bot_operador.py ' + str(update.message.chat_id))


    mainbutton = [
        ['❌ Interromper']
    ]
    
    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    mensagem = '🤖 OPERAÇÂO INICIADA \n\n'
    update.message.reply_text(mensagem, reply_markup= keyBoard1)


def interromperOperacao(update:Update, context: CallbackContext ):
    executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
    
    
    mainbutton = [
        ['🧠 Gerênciamento','⚙️ Modo de Operação'],
        ['🎯 Lista','🚨 Suporte'],
        ['🤖 Operar']
    ]

    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    message_reply_text = '🤖 Comando de interrupção enviado\n⏱️isso pode levar até 1 minuto.'
    update.message.reply_text(message_reply_text, reply_markup= keyBoard1)

    
   