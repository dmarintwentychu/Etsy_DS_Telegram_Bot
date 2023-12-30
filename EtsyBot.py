from config import *
import telebot

bot = telebot.TeleBot("6803354093:AAH9cdZtNjcNyKIECnGb2SR_Earm97PIyAE")

# Diccionario para almacenar las URLs
urls_dict = {}



def guardar_url(user_id, url):
    # Guardar la URL en el diccionario con el ID del usuario como clave
    urls_dict[user_id] = url

def comprobar_url(user_id):
    # Verificar si el usuario tiene una URL guardada
    return urls_dict.get(user_id)    


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

@bot.message_handler(commands=["comprobarurl"])
def comando_comprobar_url(message):
    # Comprobar si el usuario tiene una URL guardada
    user_id = message.from_user.id
    saved_url = comprobar_url(user_id)

    if saved_url:
        bot.reply_to(message, f"URL guardada: {saved_url}")
    else:
        bot.reply_to(message, "No se ha guardado ninguna URL")

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