import telebot
import os
import logging
from logging.handlers import RotatingFileHandler
from modules import constants, functions, handlers, drawing


# set up logging
if not os.path.exists(constants.LOG_FOLDER):
    os.makedirs(constants.LOG_FOLDER)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        RotatingFileHandler(
            os.path.join(constants.LOG_FOLDER, constants.LOG_FILE),
            maxBytes=1_000_000,
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

state = {}
user_info = {}
logger = logging.getLogger(__name__)
last_message_time = {}
bot = telebot.TeleBot(os.environ.get("BOT_KEY"))


@bot.message_handler(func=lambda message: True, commands=['help', 'start'])
def send_welcome(message):
    if not functions.max_messages_reached(message, bot, last_message_time):
        bot.send_message(
            message.chat.id,
            constants.WELCOME,
            parse_mode="HTML",
            disable_web_page_preview=True
        )


@bot.message_handler(commands=['cancelar'])
def handle_cancel(message):
    if functions.max_messages_reached(message, bot, last_message_time):
        return

    if not state or message.chat.id not in state or state[message.chat.id] < 0:
        bot.send_message(
            message.chat.id, "Ainda não há processo para ser cancelado "
            ", inicie um com o comando /placar"
        )
        return

    state[message.chat.id] = -1
    bot.send_message(
        message.chat.id, "Processo cancelado. "
        "Você pode iniciar um novo o comando /placar"
    )


@bot.message_handler(commands=['placar'])
def placar(message):
    if functions.max_messages_reached(message, bot, last_message_time):
        return

    chat_id = message.chat.id
    if state and chat_id in state and state[chat_id] >= 0:
        bot.send_message(
            chat_id=chat_id,
            text="Já existe um processo em andamento. Para começar "
            "um novo primeiramente é necessário cancelar o corrente "
            "com o comando /cancelar"
        )
        return

    state[chat_id] = -1
    bot.send_message(
        chat_id=chat_id,
        text=handlers.initialHandler[0],
        reply_markup=handlers.initialHandler[4]
    )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if functions.max_messages_reached(message, bot, last_message_time):
        return

    chat_id = message.chat.id

    if not state or chat_id not in state or state[chat_id] < -1:
        bot.send_message(
            message.chat.id,
            constants.WELCOME,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        return

    currentState = state[chat_id]

    if currentState < constants.STATE_FINAL:
        state_handler = handlers.getStateHandler(chat_id, user_info)
        bot.send_message(
            chat_id=chat_id,
            text=state_handler[currentState][0],
            reply_markup=state_handler[currentState][4]
        )
    elif currentState == constants.STATE_FINAL:
        bot.send_message(
            chat_id=chat_id,
            text=constants.DESEJA_ENVIAR_FOTO,
            reply_markup=constants.yesNoMarkup
        )
    else:
        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        photo_file = bot.download_file(photo_info.file_path)

        bot.send_message(
            chat_id=chat_id,
            text=constants.GERANDO_IMAGEM,
            reply_markup=constants.defaultMarkup
        )
        if user_info[chat_id]["tipo"].upper() == "DUPLAS":
            drawing.create_image_duplas(chat_id, user_info, bot, photo_file)
        elif user_info[chat_id]["tipo"].upper() == "TORNEIO SIMPLES":
            drawing.create_image_torneio(chat_id, user_info, bot, photo_file)
        else:
            drawing.create_image(chat_id, user_info, bot, photo_file)

        logger.info(
            (f"state len: {len(state)}\n"
             f"user_info len: {len(user_info)}\n"
             f"info: {user_info[chat_id]}")
        )

        state.pop(chat_id)


# @bot.message_handler(content_types=['text'])
@bot.message_handler(func=lambda message: True)
def process_inputs(message):
    if functions.max_messages_reached(message, bot, last_message_time):
        return

    chat_id = message.chat.id
    text = message.text.strip()

    if not state or chat_id not in state or state[chat_id] < -1:
        bot.send_message(
            message.chat.id,
            constants.WELCOME,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        return

    currentState = state[chat_id]

    if chat_id not in user_info:
        user_info[chat_id] = {}

    if currentState == -1:
        if (handlers.initialHandler[2](text)):
            user_info[chat_id][handlers.initialHandler[3]] = text
        else:
            bot.send_message(
                chat_id=chat_id,
                text=handlers.initialHandler[1],
                reply_markup=handlers.initialHandler[4]
            )
            return

    state_handler = handlers.getStateHandler(chat_id, user_info)

    if currentState == constants.STATE_FINAL:
        if functions.validate_yesNo(text):
            if text.upper() == "NÃO":
                bot.send_message(
                    chat_id=chat_id,
                    text=constants.GERANDO_IMAGEM,
                    reply_markup=constants.defaultMarkup
                )
                if user_info[chat_id]["tipo"].upper() == "DUPLAS":
                    drawing.create_image_duplas(chat_id, user_info, bot)
                elif user_info[chat_id]["tipo"].upper() == "TORNEIO SIMPLES":
                    drawing.create_image_torneio(chat_id, user_info, bot)
                else:
                    drawing.create_image(chat_id, user_info, bot)

                logger.info(
                    (f"state len: {len(state)}\n"
                     f"user_info len: {len(user_info)}\n"
                     f"info: {user_info[chat_id]}")
                )

                state.pop(chat_id)
                return
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=constants.ENVIE_FOTO,
                    reply_markup=constants.defaultMarkup
                )
                state[chat_id] = constants.WAITING_PHOTO_STATE
                return

        else:
            bot.send_message(
                chat_id=chat_id,
                text=constants.DESEJA_ENVIAR_FOTO,
                reply_markup=constants.yesNoMarkup
            )
            return
    elif currentState == constants.WAITING_PHOTO_STATE:
        bot.send_message(
            chat_id=chat_id,
            text=constants.AGUARDANDO_FOTO,
            reply_markup=constants.defaultMarkup
        )
        return

    if (state_handler[currentState][2](text)):
        user_info[chat_id][state_handler[currentState][3]] = text

        state_handler = handlers.getStateHandler(chat_id, user_info)
        state[chat_id] += 1

        if currentState + 1 < len(state_handler):
            bot.send_message(
                chat_id=chat_id,
                text=state_handler[currentState + 1][0],
                reply_markup=state_handler[currentState + 1][4]
            )
        else:
            state[chat_id] = constants.STATE_FINAL
            bot.send_message(
                chat_id=chat_id,
                text=constants.DESEJA_ENVIAR_FOTO,
                reply_markup=constants.yesNoMarkup
            )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=state_handler[currentState][1],
            reply_markup=state_handler[currentState][4]
        )


logger.info("running...")
bot.infinity_polling()
