# This Python file uses the following encoding: utf-8+
import telebot
from config import TOKEN, keys
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет, я валютный бот. Чтобы начать работу введите команду в следующем формате: \n<имя валюты> <в ' \
           'какую валюту перевести>  <количество переводимой валюты>. Чтобы посмотреть доступные валюты, ' \
           'введите /values '
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров. Введите /help для информации.')

        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Вы ошиблись. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        text = f'Стоимость {amount} {quote} равна {total_base} {base} '
        bot.send_message(message.chat.id, text)


bot.polling()
