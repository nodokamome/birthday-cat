# coding:UTF-8
import os
import asyncio
import time
import datetime
import discord
import re
import json
from collections import OrderedDict
import pprint

from discord.ext import tasks
from dotenv import load_dotenv
import datetime as dt
from datetime import datetime, date, timedelta

# .env取得
load_dotenv()

# 環境変数から取得
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = (int)(os.getenv("CHANNEL_ID"))

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 送信フラグ
isSend = True


# 挨拶大事
async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('おはようにゃ！')


# 聞いてきた人の登録情報を返す
def birthday(id):
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    for i in range(len(json_load)):
        if json_load[i]["id"] == id:
            return json_load[i]["name"]+" 誕生日"+"【"+json_load[i]["birthday"]+"】"+"欲しいものリスト: "+json_load[i]["wish"]


# 一週間後誕生日のチェック
def nextweekbirthdayCheck():
    global isSend
    today = dt.date.today()
    nextweek = today + timedelta(days=7)
    tstr1 = datetime.strftime(nextweek, '%m/%d')
    tstr2 = datetime.strftime(nextweek, '%-m/%-d')
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    for i in range(len(json_load)):
        if json_load[i]["birthday"] == tstr1 or json_load[i]["birthday"] == tstr2:
            isSend = True
            return int(i)
    return -1


# 誕生日のチェック
def birthdayCheck():
    global isSend
    today = dt.date.today()
    tstr1 = today.strftime('%m/%d')
    tstr2 = today.strftime('%-m/%-d')
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    for i in range(len(json_load)):
        if json_load[i]["birthday"] == tstr1 or json_load[i]["birthday"] == tstr2:
            isSend = True
            return int(i)
    return -1


# 全員の誕生日を表示させる
def birthdayAll():
    result = ""
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    result += "誕生日&欲しいものリスト\n------------\n"
    for i in range(len(json_load)):
        result += str(i)+"."+json_load[i]["name"]+"  " + \
            json_load[i]["birthday"]+"  " + \
            ":"+json_load[i]["wish"]+"\n"
    return result


@tasks.loop(seconds=60)
async def send_message_every_sec():
    global isSend
    channel = client.get_channel(CHANNEL_ID)
    # weekday()=0 月 weekday()=6 日
    # await channel.send("["+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+"] " + "1秒経ったよ")
    # print("["+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+"] " + "1秒経ったよ")
    if birthdayCheck() != -1 and isSend:
        json_open = open("../data/birthday.json", "r")
        json_load = json.load(json_open)
        name = json_load[birthdayCheck()]["name"]+" さん"
        await channel.send(name+"、お誕生おめでとう！\n"+"みんなでお祝いしましょう！\n"+"欲しいものリスト:"+json_load[birthdayCheck()]["wish"])
        isSend = False
    else:
        isSend = True


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
    # 「$mybirthday」→ 名前、誕生日、欲しいものリストを返す
    if message.content == '$mybirthday':
        await message.channel.send(birthday(message.author.id))
    # 「$birthday MM/DD」
    if message.content.startswith('$birthday '):
        if 1 <= len(re.findall(r'[0-9]{1,2}/[0-9]{1,2}', message.content)):
            tmp_birthday = re.findall(
                r'[0-9]{1,2}/[0-9]{1,2}', message.content)[0]
            print(tmp_birthday)
            json_open = open("../data/birthday.json", "r")
            json_load = json.load(json_open)
            for i in range(len(json_load)):
                if json_load[i]["id"] == message.author.id:
                    json_load[i]["birthday"] = tmp_birthday
                    json_open = open("../data/birthday.json", "w")
                    json_open.write(json.dumps(json_load))
                    await message.channel.send(json_load[i]["name"] + "さんの誕生日を更新しました")
    # 「$wish 」
    if message.content.startswith('$wish '):
        wish = message.content[6:]
        print(wish)
        json_open = open("../data/birthday.json", "r")
        json_load = json.load(json_open)
        for i in range(len(json_load)):
            if json_load[i]["id"] == message.author.id:
                json_load[i]["wish"] = wish
                json_open = open("../data/birthday.json", "w")
                json_open.write(json.dumps(json_load))
                await message.channel.send(json_load[i]["name"]+"さんの欲しいものを更新しました")
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
