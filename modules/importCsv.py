import requests
import csv
from io import StringIO
from telebot import types
from constants import URL_CSV


def ler_locais_csv_online(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        csvfile = StringIO(content)
        leitor = csv.DictReader(csvfile, delimiter=';')
        locais = [row['LOCAL'] for row in leitor]
        return locais
    else:
        print("Falha ao baixar o arquivo CSV")
        return []


def criar_teclado_locais(file_path):
    locais = ler_locais_csv_online(file_path)
    markup = types.ReplyKeyboardMarkup(row_width=1)
    for local in locais:
        markup.add(types.KeyboardButton(local))
    return markup


locais_disponiveis = criar_teclado_locais(URL_CSV)
