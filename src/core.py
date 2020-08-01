import telegram

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from conf.settings import BASE_API_URL, TELEGRAM_TOKEN

TELEGRAM_TOKEN='1381602607:AAESVS86drCPkaEdu1pv-UQlo8T4YHJ28cY'
BASE_API_URL='https://http.cat/'

LOJAS = [{
  "link": "https://www.carrefour.com.br/tabloide-digital?paginas=2&bolsao=RH_RJ&os=127630&width=2087&height=3701#&gid=1&pid=1",
  "cidade": "Rio_de_Janeiro",
  "loja": "Hiper Rio_Barra"
},
{
  "link": "https://www.carrefour.com.br/tabloide-digital?paginas=2&bolsao=RH_RJ&os=127630&width=2087&height=3701#&gid=1&pid=1",
  "cidade": "Rio_de_Janeiro",
  "loja": "Hiper Campo_Grande"
},

{
  "link": "https://www.carrefour.com.br/tabloide-digital?paginas=8&bolsao=FDS_SP&os=127699&width=2087&height=3701#&gid=1&pid=1",
  "cidade": "São_Paulo",
  "loja": "Hiper Brooklin"
},

{
  "link": "https://www.carrefour.com.br/tabloide-digital?paginas=19&bolsao=RH_SP&os=127494&width=1591&height=2094#&gid=1&pid=1",
  "cidade": "São_Paulo",
  "loja": "Hiper Shopping_Eldorado"
}]

def start(bot, update):
    me = bot.get_me()
    
    response_message = "Gostaria de lhe enviar o panfleto de ofertas. " \
                       "\nQual a cidade de seu interesse?" \
                       "\n/Cidade Rio_de_Janeiro" \
                       "\n/Cidade São_Paulo" \
                       "\n/Encerrar. Até breve!" \


    # Commands menu
    main_menu_keyboard = [[telegram.KeyboardButton('/Cidade Rio_de_Janeiro')],
                          [telegram.KeyboardButton('/Cidade São_Paulo')],
                          [telegram.KeyboardButton('/Encerrar')]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)

    # Send the message with menu
    bot.send_message(chat_id=update.message.chat_id,
                     text=response_message,
                     reply_markup=reply_kb_markup
    )

def http_cats(bot, update, args):
    bot.sendPhoto(
        chat_id=update.message.chat_id,
        photo=BASE_API_URL + args[0]
    )

def verificarCidade(bot, update, args):
    response_message = "Perfeito!" \
                       "\nQual a loja de seu interesse?" \
                       # "\n/Hiper Rio_Barra" \
                       # "\n/Hiper Campo_Grande" \
                       # "\n/Encerrar. Até breve!"

    for loja in LOJAS:
        #Futura versão: implementar construção do menu por seleção das lojas do parâmetro args[0]
        if (loja["cidade"] ==  args[0] == "Rio_de_Janeiro"):
            response_message += "\n/" + loja["loja"]
            main_menu_keyboard = [[telegram.KeyboardButton('/Hiper Rio_Barra')],
                                  [telegram.KeyboardButton('/Hiper Campo_Grande')],
                                  [telegram.KeyboardButton('/Encerrar')]]
        elif (loja["cidade"] == args[0] == "São_Paulo"):
            response_message += "\n/" + loja["loja"]
            main_menu_keyboard = [[telegram.KeyboardButton('/Hiper Brooklin')],
                                  [telegram.KeyboardButton('/Hiper Shopping_Eldorado')],
                                  [telegram.KeyboardButton('/Encerrar')]]
    response_message += "\n/Encerrar. Até breve!"

    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id,
                     text=response_message,
                     reply_markup=reply_kb_markup
                     )

def verificarLoja(bot, update, args):
    if((args[0]=="Rio_Barra") or (args[0]=="Campo_Grande")):
        bot.sendPhoto(
            chat_id=update.message.chat_id,
            photo="https://static.carrefour.com.br/imagens/tabloide-digital/v1/_img/impressos/127630/01_RH_RJ_127630.jpg"
        )
    elif ((args[0] == "Brooklin") or (args[0] == "Shopping_Eldorado")):
        bot.sendPhoto(
            chat_id=update.message.chat_id,
            photo="https://static.carrefour.com.br/imagens/tabloide-digital/v1/_img/impressos/127494/01_RH_SP_127494.jpg"
        )

    bot.send_message(
        chat_id=update.message.chat_id,
        text="/Start Que tal escolher outra loja?"
    )

def unknown(bot, update):
    response_message = "Desculpe, não entendi sua solicitação.\n Para reiniciar aperte o botão /Start. \n\n /Start"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )

def futureVersions(bot, update):
    response_message = "Desculpe, não entendi sua solicitação.\nEm breve ganharei a habilidade de entender a linguagem humana!"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def encerrar(bot, update):
    response_message = "Foi ótima nossa conversa de hoje. \nAproveite suas compras com o CARTÃO CARREFOUR!" \
                       "\n\n/Start"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('http', http_cats, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('Cidade', verificarCidade, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('HIPER', verificarLoja, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('Encerrar', encerrar)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.text, futureVersions)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()