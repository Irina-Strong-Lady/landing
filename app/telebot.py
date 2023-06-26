from . import bot

@bot.message_handler(commands=['Привет'])
def main(message):
    bot.send_message(message.chat.id, '<b>Добрый день, <em><u>хозяин!</u></em></b>', parse_mode='html')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')