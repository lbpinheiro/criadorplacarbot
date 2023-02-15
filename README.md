# Telegram CriadorPlacarBot

## Configurando o ambiente

1. 
```
git clone https://github.com/lbpinheiro/criadorplacarbot.git
```
2. Usand  o `.env.example` como base, crie o seu próprio `.env` e insira o TOKEN do bot
3.
```
pip install -r requirements.txt
```
4.
```
python -u criadorplacarbot.py
```

### Configurando o server

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
exec python3 criadorplacar.py
```