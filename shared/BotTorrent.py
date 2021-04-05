# -*- coding: utf-8 -*-
print("\033c")
LICENCIA = """
BOT.torrent - 1.2 :
Este programa es software GRATUITO: puedes redistribuirlo y/o modificar
bajo los términos de la Licencia Pública General GNU publicada por
la Free Software Foundation, ya sea la versión 3 de la Licencia, o
(a su elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil,
pero SIN NINGUNA GARANTÍA, ni RESPONSABILIDAD; sin siquiera la garantía implícita de
COMERCIABILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Ver el
Licencia pública general GNU para obtener más detalles <https://www.gnu.org/licenses/>.

El USUARIO de este programa, es el UNICO RESPONSABLE, de que el USO del mismo, 
se limita, al estricto cumplimiento, de cualquier LEY, aplicable.
"""
INSTALACION = """BOT.torrent - 1.2 :
*** Guía para instalar el bot ***
BOT.torrent es un sencillo script, para un BOT de Telegram, escrito en Python. 
Su función, es descargar ficheros .torrent y .zip, reenviados al BOT, en un 
directorio de nuestra elección.
Este BOT está especialmente pensado, para ejecutarse en un NAS.
Instalación:
1: Crear nuestro BOT en Telegram y obtener su TOKEN (Guías multiples en la red)
2: Instalar python3, en nuestro NAS. (Si no lo tenemos ya instalado)
3: Instalar pip en nuestro NAS, abriendo una sesión SSH, (Si no lo tenemos ya instalado) 
--> sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
--> sudo python3 get-pip.py
4: Instalar pyTelegramBotAPI --> sudo python3 -m pip install pyTelegramBotAPI
5: Copiar BOT.torrent.py, en nuestro NAS y editar las variables propias DE CADA USUARIO. 
6: Ejecutar BOT de forma interactiva --> python3 BOT.torrent.py (Por supuesto, se puede arrancar, 
tambien en background y de formar automatizada)
A disfrutar ;-)

DekkaR - 2021
"""
AYUDA = """BOT.torrent - 1.2 RC :
/ayuda      : Esta pantalla.
/start      : LICENCIA GPL, de este programa.
/instalar   : Guía para instalar este programa.
Hola        : Nos identifica y muestra nuestro ID de usuario Telegram.  
"""

# Variables DE CADA USUARIO. Modificar ######################################
# TOKEN de nuestro BOT

TOKEN = '1036849118:AAFO8UJ8Y4-V1UZfa0no2FjvYH3zYDd2Ed4'
ruta = '/share/MD0_DATA/Usb/'
rutaPDF = '/share/MD0_DATA/Usb/'
usuarios = {5426790 : 'Pruebas11'}
#############################################################################

import time
import zipfile
import os
from os import scandir, getcwd, rename
from os import remove
from functools import wraps

##############################################
# Fecha y hora
import datetime
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("BOT.torrent :", dt_string)
current_time = now.strftime("%H:%M:%S")
#############################################

import logging
# Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#############################################
import telebot # Libreria de la API Telegram.
from telebot import types
bot = telebot.TeleBot(TOKEN)

#Listener y log
def listener(messages): 
    for m in messages:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        cid = m.chat.id 
        txt = str("BOT" if m.text is None else m.text)
        if cid and cid > 0: mensaje = dt_string + ": " + m.chat.first_name  + " [" + str(cid) + "]: " + txt
        if cid and cid < 0: mensaje = dt_string + ": " + m.from_user.first_name + " [" + str(cid) + "]: " + txt
        f = open( 'log.txt', 'a') # Fichero log.
        f.write(mensaje + "\n")
        f.close()
        print(mensaje) # Mensaje --> terminal.

@bot.message_handler(commands = ['start']) 
def command_start(message): 
    cid = message.chat.id 
    time.sleep(1) 
    bot.delete_message(cid, message.message_id)
    bot.send_message( cid, LICENCIA)

@bot.message_handler(commands = ['ayuda'])
def command_ayuda(message): 
    cid = message.chat.id 
    time.sleep(1) 
    bot.delete_message(cid, message.message_id)
    if int(cid) in usuarios and message.chat.type == 'private': bot.send_message( cid, AYUDA)

@bot.message_handler(commands = ['instalar']) 
def command_instalar(message): 
    cid = message.chat.id 
    time.sleep(1) 
    bot.delete_message(cid, message.message_id)
    if int(cid) in usuarios and message.chat.type == 'private': bot.send_message( cid, INSTALACION)

# Hola --> ID Telegram
@bot.message_handler(func = lambda message: message.text == "Hola")
def command_text_hola(message): # Nos identifica
    cid = message.chat.id
    time.sleep(1)
    id_txt = "BOT .torrent: Hola!!!, " + message.from_user.first_name + '\n'
    if message.from_user.last_name: id_txt = id_txt + message.from_user.last_name + '\n'
    if message.from_user.username: id_txt = id_txt + message.from_user.username + '\n'
    id_txt = id_txt + "ID.User : " + str(message.from_user.id) + '\n'
    bot.delete_message(cid, message.message_id)
    bot.send_message(message.chat.id, id_txt)
    time.sleep(9)
    bot.delete_message(cid, message.message_id + 1)

# hola
@bot.message_handler(commands = ['hola']) 
def command_hola(message):
    cid = message.chat.id 
    bot.send_chat_action(cid, 'typing') 
    time.sleep(1)
    bot.delete_message(cid, message.message_id)
    bot.send_message( cid, "BOT.torrent:\tHola!!! " + str(message.from_user.first_name))
    time.sleep(2)
    bot.delete_message(cid, message.message_id + 1)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all(message):
    time.sleep(1)
    cid = message.chat.id
    bot.send_message(cid, "BOT.torrent ECHO: " + message.text)
    bot.delete_message(cid, message.message_id)
    time.sleep(2)
    bot.delete_message(cid, message.message_id + 1)

# Comprobamos si el mensaje es un fichero .zip.
@bot.message_handler(func = lambda message: message.document.mime_type == 'application/zip', content_types = ['document'])
def command_handle_document(message):
    cid = message.chat.id
    if int(cid) in usuarios and message.chat.type == 'private':
        archivo = bot.get_file(message.document.file_id)
        filename = message.document.file_name
        ruta_file = ruta + filename
        print(dt_string + ": " + ruta_file)
        time.sleep(1)
        downloaded_file = bot.download_file(archivo.file_path)
        with open(ruta_file,'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(cid, filename + "\nFichero Descargado!\nUsuario : " + usuarios.get(int(cid)))
        archivozip = zipfile.ZipFile(ruta_file, "r")
        for torrents in archivozip.namelist():
            if os.path.dirname(torrents) == "" and torrents.endswith('.torrent'):
                archivozip.extract(torrents, ruta)					
        archivozip.close()
        time.sleep(2)
        remove(ruta_file)	
        bot.delete_message(cid, message.message_id)
    else:
        print("Usuario NO AUTORIZADO : ", cid)
        bot.send_message(chat_id = cid, text = "No estas autorizado para utilizar el bot", parse_mode="HTML") 

# Comprobamos si el mensaje es un fichero .torrent.
@bot.message_handler(func = lambda message: message.document.mime_type == 'application/x-bittorrent', content_types = ['document'])
def command_handle_document(message):
    cid = message.chat.id
    if int(cid) in usuarios and message.chat.type == 'private':
        archivo = bot.get_file(message.document.file_id)
        filename = message.document.file_name
        ruta_file = ruta + filename
        print(dt_string + ": " + ruta_file)
        time.sleep(1)
        downloaded_file = bot.download_file(archivo.file_path)
        with open(ruta_file,'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(cid, filename + "\nFichero Descargado!\nUsuario : " + usuarios.get(int(cid)))
        time.sleep(2)
        bot.delete_message(cid, message.message_id)
    else:
        print("Usuario NO AUTORIZADO : ", cid)
        bot.send_message(chat_id = cid, text = "No estas autorizado para utilizar el bot", parse_mode="HTML") 

# Comprobamos si el mensaje es un fichero .pdf.
@bot.message_handler(func = lambda message: message.document.mime_type == 'application/pdf', content_types = ['document'])
def command_handle_document(message):
    cid = message.chat.id
    if int(cid) in usuarios and message.chat.type == 'private':
        archivo = bot.get_file(message.document.file_id)
        filename = message.document.file_name
        ruta_file = rutaPDF + filename
        print(dt_string + ": " + ruta_file)
        print("Tamaño:", archivo.file_size // 1000000)
        time.sleep(1)
        downloaded_file = bot.download_file(archivo.file_path)
        with open(ruta_file,'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(cid, filename + "\nFichero Descargado!\nUsuario : " + usuarios.get(int(cid)))
        time.sleep(2)
        bot.delete_message(cid, message.message_id)
    else:
        print("Usuario NO AUTORIZADO : ", cid)
        bot.send_message(chat_id = cid, text = "No estas autorizado para utilizar el bot", parse_mode="HTML") 


@bot.message_handler(func = lambda message: True) 
def echo_all(message):
    time.sleep(1)
    cid = message.chat.id
    bot.send_message(cid, "BOT.torrent ECHO: " + message.text)
    bot.delete_message(cid, message.message_id)
    time.sleep(2)
    bot.delete_message(cid, message.message_id + 1)

def main():
    print("BOT UP") 
 
    bot.set_update_listener(listener)

    try:
        bot.polling(none_stop = True, interval = 0, timeout = 30)
        while 1:
            time.sleep(3)
    except Exception as e:
        print("Telegram API timeout ...") 
        print(e)
        logger.critical(e)
        bot.stop_polling()
        time.sleep(30)
        print("Reboot") 
        main()

if __name__ == '__main__':
    main()