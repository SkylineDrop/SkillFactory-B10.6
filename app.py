import telebot
from config import keys
from extensions import ConvertionException, CryptoConverter
from private_config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
	text = 'Bot template to start: <currency name> \
<currency name to convert> <amount input> \n\
Получить список доступных валют: /values'
	bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def currency(message):
	text = 'Доступные валюты:'
	for key in keys.keys():
		text = '\n'.join((text, key, ))
	bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
	try:
		values = message.text.split(' ')

		if len(values) > 3:
			raise ConvertionException('Слишком много параметров')
		
		quote, base, amount = values
		total_base = CryptoConverter.get_price(quote, base, amount)
	except ConvertionException as e:
		bot.reply_to(message, f'Ошибка пользователя\n{e}')
	except Exception as e:
		bot.reply_to(message, f'Не удалось обработать команду\n{e}')
	else:
		output = f'Стоимость {amount} {quote} в {base} - {total_base}'
		bot.send_message(message.chat.id, output)


bot.polling()
