import os
import subprocess
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
        ['🤖✅ Confirmar'],
        ['Voltar']
    ]
    
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(update.message.chat_id)

    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    mensagem = '*OPERAR*\n\n'
    mensagem += '___Por favor, confirme a ordem de operação ou retorne ao menu principal e configure o robo novamente.___\n\n'

    mensagem += '*🎯 SINAIS* : ' + str(len(lista)) + '\n\n'
    
    mensagem += '*⚙️ CONFIGURAÇÂO* \n\n'
    conta = "REAL"
    if gerenciamento[0][1] == 0:
        conta = "DEMO"


    mensagem += '*Operar em conta * :' + conta + ' \n'
    mensagem += '*Delay* :' + str(gerenciamento[0][1]) + ' \n'
    mensagem += '*Valor entrada* :' + str(gerenciamento_mao_fixa[0][2]) + ' \n'
    mensagem += '*Niveis de martin-gale* :' + str(martingale[0][2]) + '\n'
    mensagem += "*Niveis de soros* :" + str(soros[0][2]) + '\n'    
    mensagem += "*Percentual de soros* :" + str(soros[0][3]) + '%\n\n'

    mensagem += '*⚠️ STOPS* \n\n'
    mensagem += "*STOP WIN* : R$ " + str(gerenciamento[0][2]) + '\n'
    mensagem += "*STOP LOSS* : R$ " +  str(gerenciamento[0][3]) + '\n'


    executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 20 where chat_id = '" + str(update.message.chat_id) + "'")
    update.message.reply_text(mensagem, reply_markup= keyBoard1, parse_mode='Markdown')


   
def cancelarOperacao(update: Update, context: CallbackContext):
    executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
    mainbutton = [
        ['🧠 Gerênciamento','⚙️ Modo de Operação'],
        ['🎯 Lista','🚨 Suporte'],
        ['🤖 Operar']
    ]

    keyBoard1 = ReplyKeyboardMarkup(mainbutton , resize_keyboard=True)
    message_reply_text = 'Menu principal'
    update.message.reply_text(message_reply_text, reply_markup= keyBoard1)

    
def confirmarOperacao(update: Update, context: CallbackContext):
    executarComando("update clientes set modo_alteracao_passo = 0, modo_alteracao = 99 where chat_id = '" + str(update.message.chat_id) + "'")
    subprocess.Popen('py bot_operador.py ' + str(update.message.chat_id))

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

    
   