# coding:UTF-8
import os
import asyncio
import time
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
TOKIMEMO_CHANNEL_ID = (int)(os.getenv("TOKIMEMO_CHANNEL_ID"))
IPPAN_CHANNEL_ID = (int)(os.getenv("IPPAN_CHANNEL_ID"))

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 送信フラグ
isCheck = True
isNextWeekCheck = True


# 挨拶大事
async def greet():
    channel = client.get_channel(TOKIMEMO_CHANNEL_ID)
    await channel.send('おはようにゃ！')


#「$mybirthday」 聞いてきた人の登録情報を返す
def mybirthday(id):
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    for i in range(len(json_load)):
        if json_load[i]["id"] == id:
            return json_load[i]["name"]+" 誕生日"+"【"+json_load[i]["birthday"]+"】"+"欲しいものリスト: "+json_load[i]["wish"]


# 一週間後誕生日のチェック
def nextweekbirthdayCheck():
    global isSend
    list = []
    today = dt.date.today()
    nextweek = today + timedelta(days=7)
    tstr1 = datetime.strftime(nextweek, '%m/%d')
    tstr2 = datetime.strftime(nextweek, '%-m/%-d')
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    for i in range(len(json_load)):
        if json_load[i]["birthday"] == tstr1 or json_load[i]["birthday"] == tstr2:
            list.append(i)
    if len(list) == 0:
        return -1
    else:
        return list


# 誕生日のチェック
def birthdayCheck():
    global isSend
    list = []
    today = dt.date.today()
    tstr1 = today.strftime('%m/%d')
    tstr2 = today.strftime('%-m/%-d')
    json_open = open("../data/birthday.json", "r")
    json_load = json.load(json_open)
    for i in range(len(json_load)):
        if json_load[i]["birthday"] == tstr1 or json_load[i]["birthday"] == tstr2:
            list.append(i)
    if len(list) == 0:
        return -1
    else:
        return list


# 「$birthdayAll」全員の誕生日を表示させる
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


def help():
    message = ""
    message += "$mybirthday: 自分の誕生日と欲しいものリスト表示\n\n"
    message += "$birthday MM/DD: 誕生日を登録\n\n"
    message += "$wish hogehoge: 欲しいものを登録。アマゾン欲しいものリストや具体例、etc\n\n"
    message += "$birthdayAll: 全員の誕生日と欲しいものリスト表示\n\n"
    message += "$neko: にゃ-ん\n\n"
    message += "$help :誕生日キャンとの使い方\n\n"
    return message


@tasks.loop(seconds=60)
async def send_message_every_sec():
    global isCheck
    global isNextWeekCheck
    tokimemo_channel = client.get_channel(TOKIMEMO＿CHANNEL_ID)
    ippan_channel = client.get_channel(IPPAN_CHANNEL_ID)
    if nextweekbirthdayCheck() != -1 and isNextWeekCheck:
        json_open = open("../data/birthday.json", "r")
        json_load = json.load(json_open)
        list = nextweekbirthdayCheck()
        for i in range(len(list)):
            name = json_load[list[i]]["name"]+" さんが\n"
            await ippan_channel.send(name+json_load[list[i]]["birthday"]+"に誕生日です。\nお祝い準備しましょう！"+json_load[list[i]]["wish"])
        isNextWeekCheck = False
    else:
        isNextWeekCheck = True
    if birthdayCheck() != -1 and isCheck:
        json_open = open("../data/birthday.json", "r")
        json_load = json.load(json_open)
        list = birthdayCheck()
        for i in range(len(list)):
            name = json_load[list[i]]["name"]+" さん"
            await ippan_channel.send(name+"、お誕生おめでとう！（誕生日:"+json_load[list[i]]["birthday"]+")\n"+"みんなでお祝いしましょう！\n"+"欲しいものリスト:"+json_load[list[i]]["wish"])
        isCheck = False
    else:
        isCheck = True


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
    # 「$mybirthday」→ 名前、誕生日、欲しいものリストを返す
    if message.content == '$mybirthday':
        await message.channel.send(mybirthday(message.author.id))
    # 「$birthday MM/DD」 → 誕生日を登録
    if message.content.startswith('$birthday '):
        if 1 <= len(re.findall(r'[0-9]{1,2}/[0-9]{1,2}', message.content)):
            tmp_birthday = re.findall(
                r'[0-9]{1,2}/[0-9]{1,2}', message.content)[0]
            print(tmp_birthday)
            json_open = open("../data/birthday.json", "r")
            json_load = json.load(json_open)
            for i in range(len(json_load)):
                if json_load[i]["id"] == message.author.id:
                    if json_load[i]["birthday"] != "":
                        await message.channel.send("誕生日がすでに登録されてますよ！\n間違えて登録した場合は、okamoさんに連絡してね")
                    else:
                        json_load[i]["birthday"] = tmp_birthday
                        json_open = open("../data/birthday.json", "w")
                        json_open.write(json.dumps(json_load))
                        await message.channel.send(json_load[i]["name"] + "さんの誕生日を更新しました")
    # 「$wish 」→ 欲しいものリストを登録
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
    # 「$birthdayAll」 → 全員の登録情報を送信
    if message.content == '$birthdayAll':
        await message.channel.send(birthdayAll())
    # 「$help」 → 誕生日キャットの使い方
    if message.content == '$help':
        await message.channel.send(help())

client.run(TOKEN)
