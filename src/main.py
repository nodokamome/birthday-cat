# coding:UTF-8
import os
import asyncio
import time
import datetime
import discord
from discord.ext import tasks
from dotenv import load_dotenv

# .env取得
load_dotenv()

# 環境変数から取得
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = (int)(os.getenv("CHANNEL_ID"))
dt_now = datetime.datetime.now()

# 接続に必要なオブジェクトを生成
client = discord.Client()

isSend = True
# 任意のチャンネルで挨拶する非同期関数を定義


async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('おはようにゃ！')


async def birthday():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('誕生！おめでとう！にゃああああああ！！！')


@tasks.loop(seconds=1)
async def send_message_every_sec():
    global isSend
    channel = client.get_channel(CHANNEL_ID)
    dt_now = datetime.datetime.now()
    # weekday()=0 月 weekday()=6 日
    # await channel.send("["+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+"] " + "1秒経ったよ")
    #print("["+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+"] " + "1秒経ったよ")
    # 準備ができたときに実行
    if datetime.date.today() == datetime.date(2020, 8, 27) and isSend:
        isSend = False
        await birthday()


@client.event
async def on_ready():
    print('Connected to Discord successfully!')
    print('------')
    await greet()
    print('おはようにゃ！')
    send_message_every_sec.start()


# メッセージ受信時に動作する処理


@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
   # 「$neko」と発言したら「にゃーん」が返る処理
    if message.content == '$neko':
        await message.channel.send('にゃーん')
    if message.content == '$date':
        dt_now = datetime.datetime.now()
        await message.channel.send(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
    if message.content == '$birthday':
        await message.channel.send("1996年3月27日")

client.run(TOKEN)
