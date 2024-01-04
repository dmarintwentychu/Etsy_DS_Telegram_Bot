from config import *
import telebot
from web_scrapping_etsy import etsyP 



bot = telebot.TeleBot("6803354093:AAH9cdZtNjcNyKIECnGb2SR_Earm97PIyAE")




def guardar_url(user_id, url):

    objeto = etsyP(url)

@bot.message_handler(commands=["start"])
def comandos(message):
    bot.reply_to(message,"Hola, ¿cómo estas?")


@bot.message_handler(commands=["guardarurl"])
def comando_guardar_url(message):
    # Obtener la URL del mensaje
    url = message.text.replace("/guardarurl ", "")

    # Guardar la URL utilizando la función
    guardar_url(message.from_user.id, url)

     # Imprimir la URL en el terminal
    print(f"URL guardada para el usuario {message.from_user.id}: {url}")

    bot.reply_to(message, f"URL guardada: {url}")

@bot.message_handler(content_types=["text"])
def mensaje (message):
    if message.text.startswith("/"):
        bot.reply_to(message, "Comando no disponible")
    else:
        bot.reply_to(message, "Texto recibido") 



if __name__ == "__main__":
    print('Iniciando el Bot')
    bot.infinity_polling()
    print('Finalizado el Bot')