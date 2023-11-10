import discord
import requests
import json
from constants import API_KEY, TOKEN
import pytz

#Parâmetros para a requisição da API
headers = {"Authorization": f"Bearer {API_KEY}",
           "Content-Type": "application/json"}
link = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo"

#Inicialização do bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Evento de inicialização do bot
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#Evento de recebimento de mensagem
@client.event
async def on_message(message):

    #Log de mensagens
    timezone = pytz.timezone("America/Sao_Paulo")
    tempo = message.created_at
    tempo = tempo.astimezone(timezone)
    tempo = tempo.strftime("%d-%m-%Y %H:%M:%S")

    with open('logs.txt', 'a', encoding="utf-8") as arquivo:
        if message.attachments:
            arquivo.write(f"[{tempo}] {message.author}: {message.attachments}" + '\n')
        else:
            arquivo.write(f"[{tempo}] {message.author}: {message.content}" + '\n')

    #Verifica se a mensagem é do próprio bot
    if message.author == client.user:
        return

    #Verifica se a mensagem começa com o prefixo estabelecido para pesquisa no GPT-3
    if message.content.startswith('serase'):
        #Envia a mensagem para a API e retorna a resposta
        mensagem = message.content.replace('serase', '')
        body = {
            "model": id_modelo,
            "messages": [{"role": "user", "content": mensagem}],
        }
        body = json.dumps(body)

        requisicao = requests.post(link, headers=headers, data=body)
        resposta = json.loads(requisicao.text)

        #Envia a resposta para o canal do Discord
        await message.channel.send(resposta['choices'][0]['message']['content'])

client.run(TOKEN)
