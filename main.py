from config import *
import telebot
import web_scrapping_etsy as etsy
from web_scrapping_etsy import etsyP 
import web_scrapping_aliexpress as ali 
import requests
import subprocess
import schedule
import time

bot = telebot.TeleBot("6803354093:AAH9cdZtNjcNyKIECnGb2SR_Earm97PIyAE")
urlGuardada = False
objeto = 0
id = 0

def guardar_url(user_id, url):
    global urlGuardada, objeto, id
    objeto = etsyP(url)
    urlGuardada = True

    caracteristicas(user_id,objeto)
    
    

def caracteristicas(user_id,objeto:etsyP):

    mensaje = ''
    envio = ''
    
    # Enviar un mensaje directo al usuario
    bot.send_message(user_id, "Las caracteristicas son las siguientes: ")

    if(objeto.isHM) :
        mensaje = 'El objeto esta fabricado a mano.\n' 
    else :
        mensaje = 'El objeto NO esta fabricado a mano.\n' 

    if(objeto.shippingCosts):
        mensaje = mensaje + 'El objeto tiene gastos de envio por: ' + str(objeto.shippingCosts) + '€.\n'
    else: 
        mensaje = mensaje + 'Los gastos de envio son gratis.\n'

    if(objeto.nReviews):
        mensaje = mensaje + 'El objeto tiene ' + str(objeto.nReviews) + ' reseñas.'
    else: 
        mensaje = mensaje + '¡CUIDADO! Este objeto no tiene reseñas o el vendedor las ha ocultado.'

    mensaje = (mensaje +  
    f'''
La tienda tiene {str(objeto.nShopRating)} reseñas.
El objeto tiene un precio de {str(objeto.price)}€.
El precio total (con gastos de envio) es de {str(objeto.totalPriece)}€.
La puntuacion total del objeto son {str(objeto.rating)} puntos.
El objeto tiene como descripcion:
{(objeto.description)}
    ''')

    bot.send_message(user_id, mensaje)
    
    

@bot.message_handler(commands=["start"])
def comandos(message):
    global id
    id = message.from_user.id
    bot.reply_to(message, "Hola, ¿cómo estas?")
    

@bot.message_handler(commands=["t"])
def comando_seguimiento(message):
    
    # Comparar precios de una url 
    url = message.text.replace("/t ", "")
    etsy.trackNewProduct(url)

@bot.message_handler(commands=["dall"])
def comando_borrarSeguimiento(message):
    # Guardamos el mensaje
    mensaje = message.text.replace("/dall ", "")
    if (mensaje==''):
        bot.reply_to(message, "¿Seguro que quieres borrar todos los seguimientos? ( /dall [si/no])")
    elif(mensaje=='si'):
        etsy.deleteJSON()
    else:
         bot.send_message(message.from_user.id, 'No se han borrado los datos')



    
def job():
    global id
    print('Empezando job...')
    mensaje = ''
    bot.send_message(id, 'Ejecutando la tarea...')
    (lowered, raised, equal) = etsy.trackListProducts()
    mensaje = 'Estos son los productos que han bajado de precio:\n'
    for i in lowered.keys() : 
        mensaje = mensaje + i + 'ha bajado a: '+ str(lowered[i])+'\n'
    bot.send_message(id, mensaje)     
    mensaje = 'Estos son los productos que han subido de precio:\n'
    for i in raised.keys() : 
        mensaje = mensaje + i + 'ha subido a: '+ str(raised[i])+'\n'
    bot.send_message(id, mensaje)     
    mensaje = 'Estos productos mantienen su precio:\n'
    for i in equal.keys() : 
        mensaje = mensaje + i + 'se mantiene en: '+ str(equal[i])+'\n'
    bot.send_message(id, mensaje) 
    print('Acabando job...')





@bot.message_handler(commands=["guardarurl"])
def comando_guardar_url(message):
    # Obtener la URL del mensaje
    url = message.text.replace("/guardarurl ", "")

    # Guardar la URL utilizando la función
    bot.reply_to(message, "Empezando Script... Esto puede llevar un momento.")
    guardar_url(message.from_user.id, url)
    bot.send_message(message.from_user.id, '¿Quieres que busque en AliExpress? ( /r [si/no] )')



@bot.message_handler(commands=["r"])
def comando_guardar_url(message):
    global urlGuardada, objeto
    # Obtener la respuesta de la pregunta
    respuesta = message.text.replace("/r ", "")
    if(urlGuardada):
        if(respuesta == 'si'):
            bot.send_message(message.from_user.id, 'Buscando en AliExpress...')
            links = ali.get_url_products(objeto.description)
            aliPList,match = ali.getInfoProducts(links,objeto)
            if (match):
                bot.send_message(message.from_user.id, 'Se ha encontrado un o mas resultados compatibles:')
            else:
                bot.send_message(message.from_user.id, 'No se han encontrado resultados compatibles\nMostrando los 5 resultados obtenidos por AliExpress...')
            for a in aliPList : 
                #response = requests.get(a.portrait)
                #bot.send_photo(message.from_user.id, response.content)
                bot.send_message(message.from_user.id, a.message())
        else:
            bot.send_message(message.from_user.id, 'Gracias por usarme.')
    else:
        bot.send_message(message.from_user.id, 'Por favor primero guarde una url.')


@bot.message_handler(commands=["stop"])
def comando_stop(message):
    bot.reply_to(message, "Deteniendo el bot...")
    # Finalizar el bot
    bot.stop_polling()

@bot.message_handler(content_types=["text"])
def mensaje(message):
    if message.text.startswith("/"):
        bot.reply_to(message, "Comando no disponible")
    else:
        bot.reply_to(message, "Texto recibido") 



if __name__ == "__main__":
    print('Iniciando el Bot')
    
    schedule.every().minute.do(job,id) 
    bot.polling()

    print('Finalizado el Bot')
    