# Telegram CriadorPlacarBot

Bot de telegram (@CriadorPlacarBot), cujo objetivo é gerar imagens com os dados de um jogo válido pelo ranking da OPEN. Ele foi desenvolvido de forma independente e não possui vínculo oficial com o ranking. O objetivo é apenas facilitar a geração da imagem.

Clique [aqui](http://t.me/CriadorPlacarBot) e acesse o bot!

## Configurando o ambiente

1. Clone este repositório 
```
git clone https://github.com/lbpinheiro/criadorplacarbot.git
```
2. Usando `.env.example` como base, crie o seu próprio `.env` e insira o TOKEN do bot
```
cp .env.example .env
```
3. Instale os requesitos
```
pip install -r requirements.txt
```
4. Inicie o servidor
```
python -u main.py
```

## Configurando o server

- Para iniciar o bot fora do service unit
```
nohup python3 -u main.py &
```

### Usando Service Unit
- Crie o service unit em `/etc/systemd/system`
```
[Unit]
Description=Criador Placar - telegram bot

[Service]
ExecStart=/usr/local/bin/telegrambot-start.sh
Restart=always

[Install]
WantedBy=multi-user.target
```
- Exemplo de script de inicialização
```
#!/bin/bash
cd /<LOCAL ONDE ESTÁ O BOT>/
exec python3 main.py
```
- A depender da fonte e da máquina utilizada como servidor, talvez seja necessário ajustes no `OFFSET` dentro do `.env`

## TODO
- Preenchimento da boleta de torneio de duplas

## Autor
[lbpinheiro](https://github.com/lbpinheiro)