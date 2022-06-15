from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler
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
import re
import os

from src.dados import retornaTodosDadosDoUsuario, verificarUsuarioTemChatLogado, VinculaContaAoChatID, configurarBaseDeDados, verificaEmailExisteBaseDeDados, entrarModoAlteracao, verificaUsuarioEmAlteracao

from src.menus.gerenciamento import entrarEmGerenciamento, alterarTipoOperacao, alterarDelay, alterarStopWin, alterarStopLoss,  alterarEmailIQ, alterarSenhaIQ
from src.menus.modooperacao import entrarEmModoOperacao, entrarEmModoMartinGale, entrarEmModoMaoFixa, alterarMaoFixa
from src.menus.lista import entrarEmLista, limparLista, adicionarLista
from src.menus.operar import entrarEmOperar,  cancelarOperacao, confirmarOperacao, interromperOperacao
#from core.usuario import verificaEmailCadastrado

updater = Updater(
    "5389773517:AAEzhBQZ5vTExZ7MsA77OzTKhtbdgjoWctM", use_context=True)

#updater = Updater("5394945805:AAFOW80oCpvDCZgGK6VrZ6U2qN_n_U6iS7o", use_context=True)


#   Processo do BOT
#   1 - Inicializar atravez do comando start
#   2 - Solicitar ao usuario o email cadastrado
#   3 -

# inicializar o processo do BOT
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Informe abaixo o seu e-mail exatamente como você colocou quando foi realizar a sua inscrição em nosso produto :")

# Usuario informou o email


def validarEmail(update: Update, context: CallbackContext):

    if not re.match(r"[^@]+@[^@]+\.[^@]+",  update.message.text):
        update.message.reply_text("Formato de email invalido.")
    else:

        existe = verificaEmailExisteBaseDeDados(
            update.message.chat_id, update.message.text)
        if(existe):

            VinculaContaAoChatID(update.message.chat_id, update.message.text)
            mainbutton = [
                ['🧠 Gerênciamento', '⚙️ Modo de Operação'],
                ['🎯 Lista', '🚨 Suporte'],
                ['🤖 Operar']
            ]
            keyBoard1 = ReplyKeyboardMarkup(mainbutton, resize_keyboard=True)
            message_reply_text = 'Seja muito bem vindo ! (Senhas em desenvolvimento)'
            update.message.reply_text(
                message_reply_text, reply_markup=keyBoard1)

        else:
            update.message.reply_text(
                "O email informado não foi encontrado em nossa base de dados.")
            update.message.reply_text(
                "Informe abaixo o seu e-mail exatamente como você colocou quando foi realizar a sua inscrição em nosso produto :")


def verificaComandosDeAlteracao(mensagem):
    alteracao = False

    if(mensagem == 'Alterar Gerenciamento' or mensagem == 'Conta IQOption'):
        alteracao = True

    if(mensagem == 'Alterar mão fixa'):
        alteracao = True

    if(mensagem == '❌ Limpar Lista' or mensagem == '✅ Adicionar Sinais'):
        alteracao = True

    if(mensagem == '🤖❌ Cancelar' or mensagem == '🤖✅ Confirmar'):
        alteracao = True

    return alteracao


def alteracao(update: Update, context: CallbackContext):

    cliente = retornaTodosDadosDoUsuario(update.message.chat_id)[0]

    # Gerenciamento
    if(cliente[0][5] == 1):
        if(cliente[0][6] == 1):
            alterarDelay(update, context)
        if(cliente[0][6] == 2):
            alterarStopWin(update, context)
        if(cliente[0][6] == 3):
            alterarStopLoss(update, context)
        if(cliente[0][6] == 4):
            alterarTipoOperacao(update, context)

    if(cliente[0][5] == 2):
        if(cliente[0][6] == 1):
            alterarEmailIQ(update, context)
        if(cliente[0][6] == 2):
            alterarSenhaIQ(update, context)

    # Operações
    if(cliente[0][5] == 3):
        if(cliente[0][6] == 1):
            alterarMaoFixa(update, context)

    # Lista
    # Operações
    if(cliente[0][5] == 10):
        if(cliente[0][6] == 1):
            limparLista(update, context)

    # adicionar itens a lista
    if(cliente[0][5] == 11):
        if(cliente[0][6] == 1):
            adicionarLista(update, context)

    # operar
    if(cliente[0][5] == 20):
        if(cliente[0][6] == 0):
            if(update.message.text == '🤖✅ Confirmar'):
                confirmarOperacao(update, context)

            if(update.message.text == '🤖❌ Cancelar'):
                cancelarOperacao(update, context)

    # operar
    if(cliente[0][5] == 99):

        if(update.message.text == '❌ Interromper'):
            interromperOperacao(update, context)
        else:
            update.message.reply_text(
                "🤖 Desculpe ! \n\nEnquanto estou em operação, não posso realizar outros comandos. Você pode interromper o serviço a qualquer momento.")


def recepcionar(update: Update, context: CallbackContext):
    # configurarBaseDeDados()

    Logado = verificarUsuarioTemChatLogado(update.message.chat_id)

    # Verifica se o usuario ja esta logado nessa conversa
    if(Logado):

        # verifica se o usuario esta fazendo alguma alteração
        if(verificaUsuarioEmAlteracao(update.message.chat_id)):
            alteracao(update, context)

        else:
            if(update.message.text == 'Voltar'):
                mainbutton = [
                    ['🧠 Gerênciamento', '⚙️ Modo de Operação'],
                    ['🎯 Lista', '🚨 Suporte'],
                    ['🤖 Operar']
                ]

                keyBoard1 = ReplyKeyboardMarkup(
                    mainbutton, resize_keyboard=True)
                message_reply_text = 'Menu Principal'
                update.message.reply_text(
                    message_reply_text, reply_markup=keyBoard1)

            else:

                # Verificar se o que o usuario esta tentando fazer é alguma alteração
                if(verificaComandosDeAlteracao(update.message.text)):

                    # 1 - Gerenciamento
                    # 2 - Conta IQOption
                    # 3 - Operação - Mão fixa
                    # 10 - Limpar lista de Sinais
                    # 11 - Adicionar lista de sinais

                    if(update.message.text == 'Alterar Gerenciamento'):
                        entrarModoAlteracao(update.message.chat_id, 1, 1)
                        update.message.reply_text(
                            "Informe o valor de Delay para cada operação :")

                    if(update.message.text == 'Conta IQOption'):
                        entrarModoAlteracao(update.message.chat_id, 2, 1)
                        update.message.reply_text(
                            "Informe seu email na IQOption :")

                    if(update.message.text == 'Alterar mão fixa'):
                        entrarModoAlteracao(update.message.chat_id, 3, 1)
                        update.message.reply_text(
                            "Informe o novo valor de mão fixa :")

                    if(update.message.text == '❌ Limpar Lista'):
                        entrarModoAlteracao(update.message.chat_id, 10, 1)
                        update.message.reply_text(
                            "Deseja realmente excluir todos os seus sinais ? isso irá interromper as ações do bot. \n\nDigite S para Sim\nDigite N para Não :")

                    if(update.message.text == '✅ Adicionar Sinais'):
                        entrarModoAlteracao(update.message.chat_id, 11, 1)
                        update.message.reply_text(
                            "Insira sua lista de sinais de acordo como foi passado para você")

                else:

                    if(update.message.text == '🧠 Gerênciamento'):
                        entrarEmGerenciamento(update, context)

                    else:
                        if(update.message.text == '⚙️ Modo de Operação' or update.message.text == 'Voltar p/ operações'):
                            entrarEmModoOperacao(update, context)
                        else:

                            # Modo de Operação ======================
                            if(update.message.text == '🖐️ Mão Fixa'):
                                entrarEmModoMaoFixa(update, context)
                            else:

                                if(update.message.text == '🎯 Lista'):
                                    entrarEmLista(update, context)
                                else:
                                    if(update.message.text == '❌ Limpar Lista'):
                                        limparLista(update, context)
                                    else:
                                        if(update.message.text == '✅ Adicionar Sinais'):
                                            adicionarLista(update, context)
                                        else:

                                            if(update.message.text == '🔂 Margin-Gale'):
                                                entrarEmModoMartinGale(
                                                    update, context)

                                            else:
                                                if(update.message.text == '🤖 Operar'):
                                                    entrarEmOperar(
                                                        update, context)
                                                 #   os.system('python operador.py ' + str(update.message.chat_id))
                                                 #   update.message.reply_text("Falha ao se comunicar com a IQOption")

                                                else:

                                                  
                                                    if not re.match(r"[^@]+@[^@]+\.[^@]+", update.message.text):
                                                        update.message.reply_text(
                                                            "Por favor informe um email válido")
                                                    else:
                                                        validarEmail(
                                                            update, context)

    else:
        validarEmail(update, context)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, recepcionar))


updater.start_polling()
print('bot iniciado')
