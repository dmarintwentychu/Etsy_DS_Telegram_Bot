from config import *
import telebot

bot = telebot.TeleBot("6803354093:AAH9cdZtNjcNyKIECnGb2SR_Earm97PIyAE")

@bot.message_handler(commands=["start"])
def comandos(message):
    bot.reply_to(message,"Hola, ¿cómo estas?")

@bot.message_handler(content_types=["text"])
def mensaje (message):
    if message.text.startswith("/"):
        bot.reply_to(message, "Comando no disponible")
    else:
        bot.reply_to(message, "Texto recibido") 



if __name__ == '__main__':
    print('Iniciando el Bot')
    bot.infinity_polling()
    print('Finalizado el Bot')