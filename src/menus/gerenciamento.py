from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
# Conter a chave da api vinda do botfather
from telegram.ext.updater import Updater
# Isso será invocado toda vez que um bot receber uma atualização
from telegram.update import Update
# Não usaremos sua funcionalidade diretamente em nosso código, mas quando adicionarmos o dispatcher, será necessário (e funcionará internamente)
from telegram.ext.callbackcontext import CallbackContext
# Esta classe Handler é usada para lidar com qualquer comando enviado pelo usuário ao bot, um comando sempre começa com “/” ou seja, “/start”,”/help” etc.
from telegram.ext.commandhandler import CommandHandler
# Esta classe Handler é usada para lidar com qualquer mensagem normal enviada pelo usuário ao bot
from telegram.ext.messagehandler import MessageHandler
# Isso filtrará texto normal, comandos, imagens, etc. de uma mensagem enviada.
from telegram.ext.filters import Filters
from src.iqcontroller import verificarSaldo
from src.dados import executarComando, retornaTodosDadosDoUsuario
import re


def entrarEmGerenciamento(update: Update, context: CallbackContext):

    banca, iqoptionConfigurado = verificarSaldo(update.message.chat_id)
    cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(
        update.message.chat_id)

    if(len(gerenciamento) == 0):
        comando = "INSERT INTO gerenciamento (delay, stop_win, stop_loss, cliente, iqoption_email, iqoption_senha, iqoption_real )"
        comando += " VALUES (  0, 0, 0, (select id from clientes where chat_id = '" + \
            str(update.message.chat_id) + "'),'', '', false);"
        executarComando(comando)
        cliente,gerenciamento,gerenciamento_mao_fixa,lista,martingale,soros = retornaTodosDadosDoUsuario(
            update.message.chat_id)

    delay = gerenciamento[0][1]
    stop_win = gerenciamento[0][2]
    stop_loss = gerenciamento[0][3]

    mainbutton = [
        ['Conta IQOption', 'Alterar Gerenciamento'],
        ['Voltar']
    ]

    acType = "Demo"
    if gerenciamento[0][5] == 1 :
        acType =  "Real"

    keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
    mensagem = '*PAINEL DE GERENCIAMENTO*\n\n'
    mensagem += '*💰 Banca* : R$ ' + str(banca) + '\n'
    mensagem += '*⏱️ Delay* : ' + str(delay) + '\n'
    mensagem += '*📈 Stop Win* : R$ ' + str(stop_win) + '\n'
    mensagem += '*📉 Stop Loss* : R$ ' + str(stop_loss) + '\n'
    mensagem += '*🤖 Operando em conta* : '+ acType +' \n'

    if iqoptionConfigurado == False:
        mensagem += '\npor favor cadastre sua conta IQOPTION'
    update.message.reply_text(
        mensagem, reply_markup=keyBoard1, parse_mode='Markdown')


def alterarDelay(update: Update, context: CallbackContext):

    try:
        if(isinstance(int(update.message.text), int)):
            executarComando("update gerenciamento set delay = " + str(update.message.text) +
                            " where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
            executarComando(
                "update clientes set modo_alteracao_passo = 2 where chat_id = '" + str(update.message.chat_id) + "'")

            update.message.reply_text("Informe um valor para Stop Win :")
        else:
            update.message.reply_text(
                "Formato de numero inválido para delay, tente novamente.")
    except:
        update.message.reply_text(
            "Formato de numero inválido para delay, tente novamente.")


def alterarStopWin(update: Update, context: CallbackContext):

    try:
        if(isinstance(int(update.message.text), int)):
            executarComando("update gerenciamento set stop_win = " + str(update.message.text) +
                            " where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
            executarComando(
                "update clientes set modo_alteracao_passo = 3 where chat_id = '" + str(update.message.chat_id) + "'")
            update.message.reply_text("Informe um valor para Stop Loss :")
        else:
            update.message.reply_text(
                "Formato de numero inválido para Stop Win, tente novamente.")
    except:
        update.message.reply_text(
            "Formato de numero inválido para Stop Win, tente novamente.")


def alterarStopLoss(update: Update, context: CallbackContext):

    try:
        if(isinstance(int(update.message.text), int)):
            executarComando("update gerenciamento set stop_loss = " + str(update.message.text) +
                            " where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
            executarComando(
                "update clientes set modo_alteracao_passo = 4 where chat_id = '" + str(update.message.chat_id) + "'")
            update.message.reply_text(
                "Deseja operar na conta Real ou Demo ? \n Digite (R) para Real e (D) para Demo :")
        else:
            update.message.reply_text(
                "Formato de numero inválido para Stop Loss , tente novamente.")
    except:
        update.message.reply_text(
            "Formato de numero inválido para Stop Loss , tente novamente.")


def alterarTipoOperacao(update: Update, context: CallbackContext):

    try:
        if(str(update.message.text).upper() == 'D' or str(update.message.text).upper() == 'R'):

            iqoption_real = True
            if str(update.message.text).upper() == 'D':
                iqoption_real = False

            executarComando("update gerenciamento set iqoption_real = "+str(iqoption_real) +
                            " where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
            executarComando(
                "update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")
            update.message.reply_text(
                "✅ Dados cadastrados com sucesso !")
            entrarEmGerenciamento(update, context)
        else:
            update.message.reply_text(
                "Deseja operar na conta Real ou Demo ? \n Digite (R) para Real e (D) para Demo :")
    except:
        update.message.reply_text(
            "Deseja operar na conta Real ou Demo ? \n Digite (R) para Real e (D) para Demo :")


def alterarEmailIQ(update: Update, context: CallbackContext):

    try:
        if re.match(r"[^@]+@[^@]+\.[^@]+",  update.message.text):
            executarComando("update gerenciamento set iqoption_email = '" + str(update.message.text) +
                            "' where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
            executarComando(
                "update clientes set modo_alteracao_passo = 2 where chat_id = '" + str(update.message.chat_id) + "'")
            update.message.reply_text("Informe sua senha na IQOption :")
        else:
            update.message.reply_text(
                "Formato de email inválido, tente novamente.")
    except:
        update.message.reply_text(
            "Formato de email inválido, tente novamente.")


def alterarSenhaIQ(update: Update, context: CallbackContext):

    try:
        executarComando("update gerenciamento set iqoption_senha = '" + str(update.message.text) +
                        "' where cliente = (select id from clientes where chat_id = '" + str(update.message.chat_id) + "')")
        executarComando(
            "update clientes set modo_alteracao_passo = 0, modo_alteracao = 0 where chat_id = '" + str(update.message.chat_id) + "'")

        update.message.reply_text(
            "✅ Dados cadastrados com sucesso !")
        entrarEmGerenciamento(update, context)
    except:
        update.message.reply_text("Falha ao alterar senha.")
