import os

# Adicionar o caminho do ffmpeg ao PATH do sistema
os.environ['PATH'] += os.pathsep + r'C:\Users\Sandro\Downloads\ffmpeg-2023-05-04-git-4006c71d19-full_build\bin'

import discord
from discord.ext import commands
import yt_dlp as youtube_dl

intents = discord.Intents.all()
intents.members = True
intents.dm_messages = True
intents.guild_messages = True

client = commands.Bot(command_prefix='?', intents=intents)

# Dicionário de opções para o youtube_dl
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'extract_flat': 'in_playlist',
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'no_warnings': True
}

# Função para obter informações sobre a música do YouTube
async def get_song_info(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            # Se o URL for uma lista de reprodução, pegue a primeira entrada
            entry = info['entries'][0]
        else:
            # Se o URL for um vídeo único, use as informações diretamente
            entry = info
        song_info = {
            'title': entry['title'],
            'source': discord.FFmpegPCMAudio(entry['url'])
        }
    return song_info

# Comando para tocar música
@client.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
        return

    try:
        song_info = await get_song_info(url)
    except Exception as e:
        await ctx.send("Não foi possível reproduzir a música.")
        print(e)
        return

    voice_client = await voice_channel.connect()
    voice_client.play(song_info['source'])
    await ctx.send(f"Tocando agora: {song_info['title']}")

# Comando para parar a reprodução de música
@client.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Reprodução de música interrompida.")
    else:
        await ctx.send("Não há música sendo reproduzida no momento.")

# Comando para fazer o bot sair do canal de voz
@client.command()
async def exit(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("Saí do canal de voz.")
    else:
        await ctx.send("Não estou conectado a nenhum canal de voz.")

# Comando para pular a música atual
@client.command()
async def skip(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        # Pula a música atual
        voice_client.stop()
        await ctx.send("Música atual pulada. Tocando a próxima música na fila.")
    else:
        await ctx.send("Não há música sendo reproduzida no momento.")

client.run('INSERT TOKEN HERE')