import telebot
import os
import requests
import json
import re
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time
from typing import NamedTuple
import copy
import logging
from logging.handlers import RotatingFileHandler

#TODO
#import inotify.adapters


# constants
VERSION = "0.1"
LOG_FOLDER = "log"
LOG_FILE = "criadorplacarbot.log"
#LOG_FILE_MAX_SIZE = 10000000 # 10 mb # TODO with inotify
MAX_MESSAGES_PER_SECOND = 4
#FONT_FILE_NAME = "cour.ttf"
FONT_FILE_NAME = "LiberationSans-Regular.ttf"
NAME_MIN = 3
NAME_MAX = 80
OFFSET = 8 #depende da fonte

JOGADOR_INVALIDO = f"O nome de um jogador deve possuir entre {NAME_MIN} e {NAME_MAX} caracteres"
WELCOME = f"""\
Seja bem-vindo ao CriadorPlacarBot! Este bot tem como objetivo gerar imagens com os dados de um jogo válido pelo ranking da OPEN. Ele foi desenvolvido de forma independente e não possui vínculo oficial com o ranking. O objetivo é apenas facilitar a geração da imagem.

Por enquanto, não há verificação de dados, como locais ou nomes de jogadores. É possível usar letras maiúsculas ou minúsculas em todos os campos.

Para iniciar, use o comando /placar. Para interromper o processo atual, use o comando /cancelar.

Para ver esta mensagem de ajuda novamente, basta usar o comando /help.

Versão {VERSION}\
"""

# boxes
# configurado para funcionar com Anchor="mm"
class FieldDimensions(NamedTuple):
    maxWidth: int
    maxHeight: int
    x: int
    y: int

TENISTA_1 = FieldDimensions(440, 69, 616, 190)
TENISTA_2 = FieldDimensions(440, 69, 616, 315)
CAT_1 = FieldDimensions(86, 77, 951, 192)
CAT_2 = FieldDimensions(86, 77, 951, 315)
PLACAR_1 = FieldDimensions(245, 130, 594, 603)
PLACAR_2 = FieldDimensions(245, 130, 594, 837)
TIEBREAK_1 = FieldDimensions(140, 130, 888, 603)
TIEBREAK_2 = FieldDimensions(140, 130, 888, 837)
LOCAL = FieldDimensions(530, 68, 674, 994)


# set up logging
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        RotatingFileHandler(os.path.join(LOG_FOLDER, LOG_FILE), maxBytes=1_000_000, backupCount=5),
        logging.StreamHandler()
    ]
)

# start
logger = logging.getLogger(__name__)
last_message_time = {}
bot = telebot.TeleBot("6056488025:AAFNBmzEdt9HTUSUD6VM19wgfj1DHZTGpwc")
user_info = {}
state = {}


def validate_name(text):
    return NAME_MIN <= len(text) <= NAME_MAX

def validate_local(text):
    return 1 <= len(text) <= 100

def validate_cat(text):
    s = text.upper()
    return s == "C" or s == "B" or s == "A" or s == "S" or s == "SS"

def validate_score(text):
    length = len(text)

    if length < 2:
        return False
    elif length == 2:
        return text == "60" or text == "61" or text == "62" or text == "63" or text == "64" or text == "75"
    else:
        pattern = r'^76\(\d+\)$'
        return re.match(pattern, text) is not None



#@bot.message_handler(commands=['help', 'start'])
@bot.message_handler(func=lambda message: True, commands=['help', 'start'])
def send_welcome(message):
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_message_time:
        time_since_last_message = current_time - last_message_time[user_id]
        if time_since_last_message < 1.0 / MAX_MESSAGES_PER_SECOND:
            bot.send_message(message.chat.id, "Muitas mensagens dentro de um curto período de tempo. Capacidade de processamento apenas de {} mensagens por segundo".format(MAX_MESSAGES_PER_SECOND))
            return
    last_message_time[user_id] = current_time

    bot.reply_to(message, WELCOME)

@bot.message_handler(commands=['cancelar'])
def handle_cancel(message):
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_message_time:
        time_since_last_message = current_time - last_message_time[user_id]
        if time_since_last_message < 1.0 / MAX_MESSAGES_PER_SECOND:
            bot.send_message(message.chat.id, "Muitas mensagens dentro de um curto período de tempo. Capacidade de processamento apenas de {} mensagens por segundo".format(MAX_MESSAGES_PER_SECOND))
            return
    last_message_time[user_id] = current_time

    if not state or message.chat.id not in state or state[message.chat.id] < 0:
        bot.send_message(message.chat.id, "Ainda não há processo para ser cancelado, inicie um com o comando /placar")
        return


    state[message.chat.id] = -1
    bot.send_message(message.chat.id, "Processo cancelado. Você pode iniciar um novo o comando /placar")

def max_font(text, width, height):
    font_size = 10
    past_font = ImageFont.truetype(FONT_FILE_NAME, font_size)
    past_bbox = past_font.getbbox(text)

    while True:
        font = ImageFont.truetype(FONT_FILE_NAME, font_size + 1)
        bbox = font.getbbox(text)
        if bbox[2] - bbox[0] > width or bbox[3] - bbox[1] > height:
            break
        font_size += 1
        past_font = copy.deepcopy(font)
        past_bbox = copy.deepcopy(bbox)

    return past_font, past_bbox

def draw_text(field, text, draw):
    font, bbox = max_font(text, field.maxWidth, field.maxHeight)
    #print(text, field.x, field.y, bbox)
    
    x = field.x
    y = field.y + OFFSET  #+ (field.maxHeight - bbox[3])/2
    draw.text((x, y), text, font=font, fill=(0, 0, 0), anchor="mm")


def create_image(chat_id):
    img = Image.open("ranking.jpg")
    draw = ImageDraw.Draw(img)

    text = user_info[chat_id]["player1"].title()
    draw_text(TENISTA_1, text, draw)

    text = user_info[chat_id]["player2"].title()
    draw_text(TENISTA_2, text, draw)
    
    text = user_info[chat_id]["cat1"].upper()
    draw_text(CAT_1, text, draw)
    
    text = user_info[chat_id]["cat2"].upper()
    draw_text(CAT_2, text, draw)
    
    score = user_info[chat_id]["score"]
    
    text = score[:1]
    draw_text(PLACAR_1, text, draw)
    
    text = score[1:2]
    draw_text(PLACAR_2, text, draw)
    
    if len(score) > 2:
        match = re.search(r"\((\d+)\)", score)
        tie2 = int(match.group(1))
        tie1 = 7

        if tie2 > 5:
            tie1 = tie2 + 2

        #tiebreak 1
        text = str(tie1)
        draw_text(TIEBREAK_1, text, draw)

        #tiebreak 2
        text = str(tie2)
        draw_text(TIEBREAK_2, text, draw)
        
    #local
    text = user_info[chat_id]["local"].upper()
    draw_text(LOCAL, text, draw)

    # Save the image
    img_file_name = "{chat}-{date}.jpg".format(chat=chat_id, date=datetime.today().strftime('%Y-%m-%d'))
    img.save(img_file_name)

    with open(img_file_name, 'rb') as f:
        bot.send_photo(chat_id=chat_id, photo=f)

    logger.info(f"removing image {img_file_name}, chat_id={chat_id}, user_info={user_info[chat_id]}")

    try:
        os.remove(img_file_name)
    except OSError as e:
        logger.error(f"Error while deleting file: {e}")


stateHandler = [
    ("Insira o nome do jogador vencedor", JOGADOR_INVALIDO, validate_name, "player1"),
    ("Insira a categoria do jogador vencedor (C, B, A, S ou SS)", "Categoria Inválida. As categorias válidas são C, B, A, S ou SS", validate_cat, "cat1"), 
    ("Insira o nome do jogador derrotado", JOGADOR_INVALIDO, validate_name, "player2"),
    ("Insira a categoria do jogador derrotado (C, B, A, S ou SS)", "Categoria Inválida. As categorias válidas são C, B, A, S ou SS", validate_cat, "cat2"), 
    ("Insira o placar do jogo, sempre em referência ao vencedor e apenas números. Exemplos: 60, 63, 75. Em caso de tiebreak, informe os pontos do perdedor entre parênteses, exemplos: 76(4), 76(9)", "Placar inválido", validate_score, "score"),
    ("Insira o nome do local onde ocorreu o jogo", "Local inválido", validate_local, "local")
]

@bot.message_handler(commands=['placar'])
def placar(message):
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_message_time:
        time_since_last_message = current_time - last_message_time[user_id]
        if time_since_last_message < 1.0 / MAX_MESSAGES_PER_SECOND:
            bot.send_message(message.chat.id, f"Muitas mensagens dentro de um curto período de tempo. Capacidade de processamento apenas de {MAX_MESSAGES_PER_SECOND} mensagens por segundo")
            return
    last_message_time[user_id] = current_time


    chat_id = message.chat.id
    if state and chat_id in state and state[chat_id] >= 0:
        bot.send_message(chat_id=chat_id, text="Já existe um processo em andamento. Para começar um novo primeiramente é necessário cancelar o corrente com o comando /cancelar")
        return

    state[chat_id] = 0
    bot.send_message(chat_id=chat_id, text=stateHandler[state[chat_id]][0])
    
    #bot.register_next_step_handler(message, process_player1)


#@bot.message_handler(content_types=['text'])
@bot.message_handler(func=lambda message: True)
def process_inputs(message):

    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_message_time:
        time_since_last_message = current_time - last_message_time[user_id]
        if time_since_last_message < 1.0 / MAX_MESSAGES_PER_SECOND:
            bot.send_message(message.chat.id, f"Muitas mensagens dentro de um curto período de tempo. Capacidade de processamento apenas de {MAX_MESSAGES_PER_SECOND} mensagens por segundo")
            return
    last_message_time[user_id] = current_time
    # Your code that handles the message
    #bot.send_message(message.chat.id, "Your message was received!")


    chat_id = message.chat.id
    text = message.text.strip()
    
    if not state or chat_id not in state or state[chat_id] < 0:
        bot.send_message(chat_id=chat_id, text=WELCOME)
        return

    currentState = state[chat_id]
    
    if chat_id not in user_info:
        user_info[chat_id] = {}

    if currentState == len(stateHandler):
        bot.send_message(chat_id=chat_id, text="para começar uma nova geração de placar, use novamente o comando /placar")
        return

    if (stateHandler[currentState][2](text)):
        #print("adding " + text + " into key " + stateHandler[currentState][3])
        user_info[chat_id][stateHandler[currentState][3]] = text
        #print(user_info[chat_id])

        state[chat_id] += 1
        
        if currentState + 1 < len(stateHandler):
            bot.send_message(chat_id=chat_id, text=stateHandler[currentState + 1][0])
        else:
            bot.send_message(chat_id=chat_id, text="criando a imagem, pode demorar alguns segundos ...")
            create_image(chat_id)
            logger.info("state len: {}\nuser_info len: {}".format(len(state), len(user_info)))
            state[chat_id] = -1
            #bot.send_message(chat_id=chat_id, text="acabou")

    else:
        bot.send_message(chat_id=chat_id, text=stateHandler[currentState][1])

logger.info("running...")
bot.polling()