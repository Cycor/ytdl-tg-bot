#https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
#https://github.com/eternnoir/pyTelegramBotAPI/blob/master/README.md#a-simple-echo-bot
#tgtoken="TG-BOT-TOKEN" tgchatid="TG-CHAT-ID" ytdldir="/PATH/TO/DOWNLOAD/DIR" python3 bot.py

from __future__ import unicode_literals
import telebot
import youtube_dl
import os

# import logging
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

for env in ["tgtoken","tgchatid","ytdldir"]:
  if env not in os.environ:
    print(env + ' not found')
    exit()

bot = telebot.TeleBot(os.getenv('tgtoken'))
chat_id = int(os.getenv('tgchatid'))
ytdldir = os.getenv('ytdldir')

class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        #print(msg)
        bot.send_message(chat_id, msg)

def my_hook(d):
    if d['status'] == 'finished':
        bot.send_message(chat_id, 'finished:\n' + d['filename'])
    if d['status'] == 'error':
        bot.send_message(chat_id, 'error:\n' + d['filename'])

ydl_opts = {
    'format': 'best',
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

@bot.message_handler(func=lambda message: message.chat.id == chat_id)
def echo_all(message):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        bot.reply_to(message, 'downloading')
        ydl.download([message.text])

bot.polling()


