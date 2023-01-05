import telebot
from config import keys, TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", ])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Что умеет этот бот? \n\nПозволяет быстро конвертировать с одной валюты в другую.\
    \n\nДля просмотра списка всех доступных валют введите /values \n\nЧтобы вызвать инструкцию введите /help")


@bot.message_handler(commands=["help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду в следующем формате: \n<название конвертируемой валюты> \
<название валюты, в которую конвертируем> \
<количество переводимой валюты>."
    print(message.text)
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message):
    try:
        values = message.text.split()
        if len(values) < 3:
            raise APIException("Введены не все необходимые параметры")
        elif len(values) > 3:
            raise APIException("Введено больше параметров, чем требуется")

        quote, base, amount = values
        quote = quote.lower()
        base = base.lower()

        sum = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n {e}")
    else:
        text = f'Стоимость {amount} {keys[quote]} = {sum} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
