#!/usr/bin/env python

from __future__ import unicode_literals
import youtube_dl
import re
from os import environ, getenv
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        notify(msg)

def my_hook(d):
    if d['status'] == 'finished':
        notify('finished:\n' + d['filename'] + '\nsize: ' + str(round(d['total_bytes'] / 1024 / 1024,1)) + 'MB')
    if d['status'] == 'error':
        notify('error:\n' + d['filename'])

def download(url,update):
    opts = {
        'format': 'best',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'ignoreerrors': True,
        'nooverwrites': True,
        'continuedl': True,
        'youtube_include_dash_manifest': False,
        'socket_timeout': 8,
        'retries': 3,
        'outtmpl': getenv('ytdldir') + '/%(title)s-%(id)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        update.message.reply_text('format:' + opts['format'] + '\ndownloading',quote=True)
        try:
            ydl.download([url])
        except:
            update.message.reply_text('Unexpected error occurred',quote=True)

def notify(msg:str):
    bot = Bot(token=getenv('tgtoken'))
    bot.send_message(chat_id=getenv('tgchatid'), text=msg)

def urlhandler(update: Update, context: CallbackContext):
    urlmatch = re.match('^.*(https?://[\S]+).*$',update.message.text,re.I)
    if not urlmatch:
        update.message.reply_text("Show me the URL")
        return
    url = urlmatch.group(1)
    download(url,update)

def main():
    for env in ["tgtoken","tgchatid","ytdldir"]:
        if env not in environ:
            print(env + ' not found')
            exit(1)
    del env
    updater = Updater(getenv('tgtoken'))
    idflt = Filters.chat(int(getenv('tgchatid')))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(idflt, urlhandler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
