import requests
import csv
from io import StringIO


# utilizada apenas para testes locais
def ler_locais_csv_local(caminho_arquivo):
    try:
        with open(caminho_arquivo, newline='',
                  encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv, delimiter=';')
            locais = [[row['LOCAL'], row['LOCAL2']] for row in leitor]
            return locais
    except FileNotFoundError:
        print(f"Arquivo CSV não encontrado: {caminho_arquivo}")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return []


def ler_locais_csv_online(url):
    response = requests.get(url)

    if response.status_code == 200:
        content = response.content.decode('utf-8')
        csvfile = StringIO(content)
        leitor = csv.DictReader(csvfile, delimiter=';')
        locais = [[row['LOCAL'], row['LOCAL2']] for row in leitor]
        return locais
    else:
        print("Falha ao baixar o arquivo CSV")
        return []
