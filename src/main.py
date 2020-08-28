# coding:UTF-8
import os
import asyncio
import time
import datetime
import discord
import json
from collections import OrderedDict
import pprint

from discord.ext import tasks
from dotenv import load_dotenv
from datetime import datetime as dt

json_open = open("../data/birthday.json", "r")
json_load = json.load(json_open)
for i in range(len(json_load)):
    print(str(i) + "." + json_load[i]["name"] + ":" + json_load[i]["birthday"])
    if json_load[i]["birthday"] == datetime.date.today():
        print("誕生日おめでとう")


# .env取得
load_dotenv()

# 環境変数から取得
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = (int)(os.getenv("CHANNEL_ID"))
dt_now = datetime.datetime.now()

# 接続に必要なオブジェクトを生成
client = discord.Client()

isSend = True


# 挨拶大事
async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('おはようにゃ！')


def birthday(id):
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    for i in range(len(json_load)):
        # if json_load[i]["birthday"] == datetime.date.today():
        if json_load[i]["id"] == id:
            return json_load[i]["name"]+" 誕生日"+"【"+json_load[i]["birthday"]+"】"+"欲しいものリスト: "+json_load[i]["wish"]


def birthdayAll():
    result = ""
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    result += "誕生日&欲しいものリスト\n------------\n"
    for i in range(len(json_load)):
        # if json_load[i]["birthday"] == datetime.date.today():
        result += str(i)+"."+json_load[i]["name"]+"  " + \
            json_load[i]["birthday"]+"  " + \
            ":"+json_load[i]["wish"]+"\n"
    return result


@ tasks.loop(seconds=1)
async def send_message_every_sec():
    global isSend
    channel = client.get_channel(CHANNEL_ID)
    dt_now = datetime.datetime.now()
    # weekday()=0 月 weekday()=6 日
    # await channel.send("["+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+"] " + "1秒経ったよ")
    # print("["+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+"] " + "1秒経ったよ")
    # 準備ができたときに実行
    if datetime.date.today() == datetime.date(2020, 8, 27) and isSend:
        isSend = False


# 起動時
@ client.event
async def on_ready():
    print('Connected to Discord successfully!')
    print('------')
    # 挨拶をした後に、誕生日チェックが始まる
    await greet()
    send_message_every_sec.start()


# メッセージ受信時に動作する処理
@ client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「$neko」→「にゃーん」と返す
    if message.content == '$neko':
        await message.channel.send('にゃーん')
    # 「$date」→ 日付を返す('%Y年%m月%d日 %H:%M:%S')
    if message.content == '$date':
        dt_now = datetime.datetime.now()
        await message.channel.send(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
    # 「$birthday」→ 名前、誕生日、欲しいものリストを返す
    if message.content == '$birthday':
        await message.channel.send(birthday(message.author.id))
    if message.content == '$birthday':
        await message.channel.send(birthday(message.author.id))
    if message.content == '$birthday-all':
        await message.channel.send(birthdayAll())
    if message.content == '$hello':
        tdatetime = dt.now()
        tstr = tdatetime.strftime('%m/%d')
        print(tstr)
        json_open = open("../data/birthday.json", "r")
        json_load = json.load(json_open)
        for i in range(len(json_load)):
            # if json_load[i]["birthday"] == datetime.date.today():
            if json_load[i]["birthday"] == tstr:
                await message.channel.send(message.author.mention+" "+json_load[i]["name"]+"さん、"+"誕生日おめでとう！！")

client.run(TOKEN)
