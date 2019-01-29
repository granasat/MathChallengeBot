# -*- coding: utf-8 -*-
import telebot
from telebot import types
import requests
import os
from enqueuer import EventQueue
from ESCPOS import *
from PIL import Image
import wget
import csv
import datetime

# Set up the printer serial Port
try:
    t = Thermal("/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0")
except:
    t = None

# Create a queue that will print the tasks as soon as the enter in the queue
eq = EventQueue()

# Token from bot father on telegram
# ejecutar /newbot
#
# USING ENV VARIABLES, PUT YOUR TOKEN HERE AS `API_TOKEN = "TOKEN"`
API_TOKEN = os.environ['TELEBOT_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

# Get current date for displaying in our program
now = datetime.datetime.now()
FECHA = str(now.day) + "/" + str(now.month) + "/" + str(now.year)


class User:
    def __init__(self, name):
        self.name = name
        self.apellidos = None
        self.curso = None
        self.centro = None
        self.ciudad = None
        self.mail = None
        self.challenge = None # Bool that indicates if the user solve the challenge


def add_data_csv(user,imgPath):
    #print("Writing Data: " + user.name + " " + user.apellidos + " " + user.curso + " " + user.centro + " " + user.ciudad + " " + user.mail)
    fields = [str(user.name), str(user.apellidos), str(user.curso), str(user.centro), str(user.ciudad), str(user.mail), str(imgPath)]
    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    f.close()


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("º", "o"),
        ("ñ", "\xA4"),
        ("Ñ", "\xA5"),
        ("¿", "\xA8")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def printTicket(userImg, user, imgPath):      #Pic, user data, and a bool that indicates if the user solved the challenge
    # Añadimos la info de usuario al CSV
    add_data_csv(user,imgPath)

    print("Imprimiendo foto")

    t.println("")
    t.println("")
    t.println("")
    im = Image.open("logo.jpg")
    t.textAlignCenter(im.size[0])
    t.printOldBitmap(im)
    t.resetAlign()
    t.println("")
    t.println("   \xA8Quiero ser ingeniera?")
    t.textAlignCenter(100)
    t.println(FECHA)
    t.resetAlign()
    t.textAlignCenter(userImg.size[0])
    t.printOldBitmap(userImg)
    t.resetAlign()
    t.println("")
    t.println("")
    t.setMargin(10)     # 10 mm margin
    t.set_print_density(10)
    t.println(normalize("Nombre: " + str(user.name)))
    t.set_print_density(0)
    t.println(normalize("Apellidos: " + str(user.apellidos)))
    t.println(normalize("Curso: " + str(user.curso)))
    t.println(normalize("Centro: " + str(user.centro)))
    t.println(normalize("Ciudad: " + str(user.ciudad)))
    t.println(normalize("Email: " + str(user.mail)))

    t.println("")
    t.println("")

    t.setMargin(21)
    t.println("-Reto-")
    t.setMargin(5)
    t.println(normalize("Rosi es 3 años mayor que Lili. Toto tiene la mitad de años que Rosi. Lili tiene 11 años"))
    t.println(normalize("¿Cuátos años tiene Toto?"))
    t.println("")

    t.setMargin(20)
    t.println(normalize("Solución: 7 años"))
    t.setMargin(5)

    if user.challenge:
        t.println(normalize("Superaste el reto!"))
        t.resetAlign()
        im = Image.open("good.jpg")
        t.textAlignCenter(im.size[0])
        t.printOldBitmap(im)
        t.resetAlign()
    else:
        t.println(normalize("No has superado el reto, pero siempre estará septiembre"))
        im = Image.open("bad.jpg")
        t.textAlignCenter(im.size[0])
        t.printOldBitmap(im)
        t.resetAlign()

    t.setMargin(10)      # 10 mm margin left
    t.println("https://granasat.ugr.es")
    t.println("")
    t.println("")
    t.println("")
    t.setMargin(17)  # 10 mm margin
    t.println("Aerospace Group GranaSAT")
    t.textAlignCenter(50)
    t.println("Orbiting your mind")
    t.resetAlign()
    t.println(normalize("Thanks to Fran Acién and Pablo Garrid"))
    t.resetAlign()
    t.println("")
    t.println("")
    t.println("")
    t.println("")
    t.cutPaper()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hola!")
    markup = types.ForceReply(selective=False)
    msg = bot.send_message(message.chat.id, "Hola! Dime tu nombre!", reply_markup=markup)

    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    try:
        chat_id = message.chat.id
        name = message.text.encode('utf-8')
        user = User(name)
        user_dict[chat_id] = user
        markup = types.ForceReply(selective=False)
        msg = bot.reply_to(message, '¿Cómo te apellidas?', reply_markup=markup)
        bot.register_next_step_handler(msg, get_apellidos)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def get_apellidos(message):
    try:
        chat_id = message.chat.id
        apellidos = message.text.encode('utf-8')
        user = user_dict[chat_id]
        user.apellidos = apellidos
        markup = types.ForceReply(selective=False)
        msg = bot.reply_to(message, '¿De qué curso eres?', reply_markup=markup)
        bot.register_next_step_handler(msg, get_curso)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def get_curso(message):
    try:
        chat_id = message.chat.id
        curso = message.text.encode('utf-8')
        user = user_dict[chat_id]
        user.curso = curso
        markup = types.ForceReply(selective=False)
        msg = bot.reply_to(message, '¿De qué centro eres?', reply_markup=markup)
        bot.register_next_step_handler(msg, get_centro)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def get_centro(message):
    try:
        chat_id = message.chat.id
        centro = message.text.encode('utf-8')
        user = user_dict[chat_id]
        user.centro = centro
        markup = types.ForceReply(selective=False)
        msg = bot.reply_to(message, '¿De qué ciudad eres?', reply_markup=markup)
        bot.register_next_step_handler(msg, get_ciudad)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def get_ciudad(message):
    try:
        chat_id = message.chat.id
        ciudad = message.text.encode('utf-8')
        user = user_dict[chat_id]
        user.ciudad = ciudad
        markup = types.ForceReply(selective=False)
        msg = bot.reply_to(message, '¿Cuál es tu mail?', reply_markup=markup)
        bot.register_next_step_handler(msg, get_mail)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def get_mail(message):
    try:
        chat_id = message.chat.id
        mail = message.text.encode('utf-8')
        user = user_dict[chat_id]
        user.mail = mail

        bot.send_message(chat_id, "¿Aceptarías un reto matemático?")
        bot.send_message(chat_id, "Rosi es 3 años mayor que Lili\nToto tiene la mitad de años que Rosi\nLili tiene 11 años\n")

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('6', '7', '8', '12')
        msg = bot.send_message(chat_id, '¿Cuál es la de edad de Toto?', reply_markup=markup)
        bot.register_next_step_handler(msg, resolver_problema)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def resolver_problema(message):
    try:
        chat_id = message.chat.id
        respuesta = message.text.encode('utf-8')
        user = user_dict[chat_id]

        if respuesta == '7':
            user.challenge = True
            bot.reply_to(message, "Correcto")
        else:
            user.challenge = False
            bot.reply_to(message, "Métete a letras")

        msg = bot.send_message(chat_id, "Enviame una foto!")
        bot.register_next_step_handler(msg, process_pic)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_pic(message):
    if message.content_type != "photo":
        bot.reply_to(message, "Lo que me has enviado no es una foto!")
        msg = bot.reply_to(message, 'Enviame una foto!')
        bot.register_next_step_handler(msg, process_pic)
    else:
        bot.reply_to(message, "Muchas graciass")

        chat_id = message.chat.id
        user = user_dict[chat_id]


        #print("New foto " + message.photo)
        fileID = message.photo[-1].file_id
        file = bot.get_file(fileID)
        print 'file.file_path =', file.file_path
        url_pic_path = "https://api.telegram.org/file/bot" + API_TOKEN + "/" + file.file_path
        print(url_pic_path)
        output = os.path.join("photos/", str(message.message_id) + ".jpg")
        wget.download(url=url_pic_path, out=output)

        eq.enqueue(printTicket, [Image.open(output), user, output])

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "Para utilizar el bot envia /start")

bot.polling()


#Web Server
import os
from flask import Flask, request, send_from_directory, send_file

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/images/<filename>')
def serve_images(filename):
    return send_file("photos/" + filename)

@app.route('/<path:filename>')  
def serve_static(filename):  
    return send_from_directory("imagesWebApp", filename)

@app.route("/data")
def data():
    root_dir = os.path.dirname(os.getcwd())
    return send_file("data.csv")

@app.route("/")
def hello():
    return send_file("imagesWebApp/index.html")

if __name__ == "__main__":
    app.run()

