import time
import re
from modules import constants
from modules import importCsv

#if not constants.locais_jogos:
    # Chama a função para inicializar locais_jogos
    #constants.locais_jogos = importCsv.ler_locais_csv_online(constants.URL_CSV)
# def remover_acentos_preservar_cedilha(texto):
    # Mapeamento personalizado para preservar o caractere 'ç'
 #   mapa_personalizado = {
 #       'c': 'ç'
  #  }

    # Aplica unidecode, mas preserva o 'ç'
   # texto_sem_acentos = ''.join(map(lambda char: mapa_personalizado.get(char, unidecode(char)), texto))

    #return texto_sem_acentos

def validate_tipo(text):
    s = text.upper()
    return s in {"SIMPLES", "DUPLAS", "TORNEIO SIMPLES"}


def validate_name(text):
    return constants.NAME_MIN <= len(text) <= constants.NAME_MAX


def validate_local(text):
    text_upper = text.upper()
    
    for local in constants.locais_jogos:
        if text_upper == local[0] or text_upper == local[1]:
            return True

    return False


def validate_cat(text):
    s = text.upper()
    return s in {"C", "B", "A", "S", "SS"}


def validate_score(text):
    length = len(text)

    if length < 2:
        return False
    elif length == 2:
        return text in {"60", "61", "62", "63", "64", "75"}
    else:
        pattern = r'^76\(\d+\)$'
        return re.match(pattern, text) is not None


def validate_score_torneio(text):
    sets = text.strip().split()
    sets_size = len(sets)
    if sets_size < 2 or sets_size > 3:
        return False

    tenista1_sets_vencidos = 0
    for i in range(2):
        if sets[i] in {"60", "61", "62", "63", "64", "75", "76"}:
            tenista1_sets_vencidos += 1
        elif sets[i] not in {"06", "16", "26", "36", "46", "57", "67"}:
            return False

    if tenista1_sets_vencidos == 2:
        return sets_size == 2
    elif tenista1_sets_vencidos == 0:
        return False
    elif tenista1_sets_vencidos == 1 and sets_size != 3:
        return False

    # terceiro set é um tiebreak, número de pontos do tenista perdedor
    return sets[2].isdigit()


def validate_yesNo(text):
    upperText = text.upper()
    return upperText == "SIM" or upperText == "NÃO"


def max_messages_reached(message, bot, lastMessage_obj):
    current_time = time.time()
    user_id = message.from_user.id
    ret = False
    if user_id in lastMessage_obj:
        time_since_last_message = current_time - lastMessage_obj[user_id]
        if time_since_last_message < 1.0 / constants.MAX_MESSAGES_PER_SECOND:
            bot.send_message(
                message.chat.id,
                (f"Muitas mensagens dentro de um curto período de tempo."
                 f" Capacidade de processamento apenas de"
                 f" {constants.MAX_MESSAGES_PER_SECOND} mensagens por segundo")
            )
            ret = True

    lastMessage_obj[user_id] = current_time
    return ret
