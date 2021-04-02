# https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
# https://github.com/eternnoir/pyTelegramBotAPI/blob/master/README.md#a-simple-echo-bot

# run:
# pip3 install pyTelegramBotAPI youtube-dl
# tgtoken="TG-BOT-TOKEN" tgchatid="TG-CHAT-ID" ytdldir="/PATH/TO/DOWNLOAD/DIR" python3 bot.py

from __future__ import unicode_literals
import telebot
import youtube_dl
import os
import gc
gc.enable()

# import logging
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

for env in ["tgtoken","tgchatid","ytdldir"]:
    if env not in os.environ:
        print(env + ' not found')
        exit()
del env

bot = telebot.TeleBot(os.getenv('tgtoken'))
chat_id = int(os.getenv('tgchatid'))
ytdldir = os.getenv('ytdldir')

class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        bot.send_message(chat_id, msg)

def my_hook(d):
    if d['status'] == 'finished':
        bot.send_message(chat_id, 'finished:\n' + d['filename'] + '\nsize: ' + str(round(d['total_bytes'] / 1024 / 1024,1)) + 'MB')
    if d['status'] == 'error':
        bot.send_message(chat_id, 'error:\n' + d['filename'])

def msg_filter(message):
    if message.chat.id != chat_id:
        return False
    if message.content_type != 'text':
        bot.reply_to(message, 'text only')
        return False
    return True

def ydl_opts(message):
    dlfmt='best'
    dlurl = message.text
    if dlurl[-6:] == ' audio':
        dlurl = dlurl[:-6]
        dlfmt = 'bestaudio'
    opts = {
        'format': dlfmt,
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'ignoreerrors': True,
        'nooverwrites': True,
        'continuedl': True,
        'youtube_include_dash_manifest': False,
        'socket_timeout': 8,
        'retries': 3,
        'outtmpl': ytdldir + '/%(title)s-%(id)s.%(ext)s',
    }
    return opts, dlurl

@bot.message_handler(func=msg_filter)
def download(message):
    opts, dlurl = ydl_opts(message)
    with youtube_dl.YoutubeDL(opts) as ydl:
        bot.reply_to(message, 'format:' + opts['format'] + '\ndownloading')
        try:
            ydl.download([dlurl])
        except:
            bot.reply_to(message, 'Unexpected error occurred')

bot.polling()
