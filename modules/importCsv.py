import requests
import csv
from io import StringIO
from telebot import types

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
    locais = ler_locais_csv_online(file_path)  # Lê os locais do arquivo CSV
    markup = types.ReplyKeyboardMarkup(row_width=1)
    for local in locais:
        markup.add(types.KeyboardButton(local))  # Adiciona cada local como um botão no teclado de resposta
    return markup

# URL do arqutps://rivo CSV online
url_csv = 'https://raw.githubusercontent.com/zani19/criadorplacarbot/main/locais/Locais%20dos%20Jogos%20-%20Nomes%20Padr%C3%A3o%20031223.csv'

# Criar teclado de resposta a partir do arquivo CSV online
locais_disponiveis = criar_teclado_locais(url_csv)
