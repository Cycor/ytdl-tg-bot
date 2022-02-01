#!/usr/bin/env python

from __future__ import unicode_literals
import pprint
import yt_dlp
import re
import time
from os import environ, getenv
from telegram import Update, Bot, Message
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


class Telegram:

    def __init__(self, token: str, chatid: int):
        self.token = token
        self.chatid = chatid
        self.bot = Bot(self.token)

        self.updater = Updater(getenv('tgtoken'))
        idflt = Filters.chat(int(getenv('tgchatid')))
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(MessageHandler(idflt, self.message_handler))

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    def send_message(self, text: str) -> Message:
        print("send_message: " + text, flush=True)
        return self.bot.send_message(chat_id=self.chatid, text=text)

    def edit_message(self, message: Message, text: str) -> Message:
        self.bot.edit_message_text(text=text, chat_id=message.chat_id, message_id=message.message_id)
        return message

    def message_handler(self, update: Update, context: CallbackContext):
        if not update.message:
            return

        print(f"Received: {update.message.text}", flush=True)

        urlmatch = re.match('^.*(https?://[\S]+).*$', update.message.text, re.I)
        if not urlmatch:
            update.message.reply_text("Show me the URL")
            return
        url = urlmatch.group(1)

        MyDownloader(update, self).download(url)


class MyDownloader:

    def __init__(self, update: Update, telegram_bot: Telegram):
        self.update = update
        self.telegram_bot = telegram_bot
        self.status_msg = None
        self.last_msg_time = time.time()
        self.yt_info = None

    def my_hook(self, d):
        if d['status'] == 'finished':
            # self.telegram_bot.send_message(f"finished downloading, starting convert:\n{d['filename']}\nsize: {str(round(d['total_bytes'] / 1024 / 1024, 1))}MB")
            # self.update.message.reply_text(f"finished downloading, starting convert:\n{d['filename']}\nsize: {str(round(d['total_bytes'] / 1024 / 1024, 1))}MB")
            # pprint.pprint(d)
            self.yt_info = d["info_dict"]

        if d['status'] == 'downloading':
            print(d['filename'], d['_percent_str'], d['_eta_str'])

            filetype = "unknown"
            if d['info_dict']['acodec'] != 'none':
                filetype = "audio"
                if d['info_dict']['vcodec'] != 'none':
                    filetype = "audio+video"
            elif d['info_dict']['vcodec'] != 'none':
                filetype = "video"

            if (self.status_msg and time.time() - self.last_msg_time) > 5:
                self.telegram_bot.edit_message(self.status_msg, f'Downloading {filetype}... {d["_percent_str"]}')
                self.last_msg_time = time.time()

        if d['status'] == 'error':
            # self.telegram_bot.send_message(f"error:\n{d['filename']}")
            self.update.message.reply_text(f"error:\n{d['filename']}")

    def download(self, url):
        self.last_msg_time = time.time()

        ytdldir = getenv('ytdldir')

        opts = {
            'format': getenv('format'),
            'logger': MyLogger(self.telegram_bot),
            'progress_hooks': [self.my_hook],
            'ignoreerrors': True,
            'overwrites': True,
            'nopostoverwrites': True,
            'continuedl': True,
            'writeinfojson': True,
            'writethumbnail': True,
            'check_formats': 'selected',
            'merge_output_format': 'mp4',
            'subtitleslangs': 'en.*,nl.*,du.*,-live_chat',
            'sleep_interval': 2,
            'socket_timeout': 8,
            'retries': 3,
            'noplaylist': True,
            'paths': {"temp": "/tmp", "home": ytdldir},
            'postprocessors': [{
                # Embed metadata in video using ffmpeg.
                'key': 'FFmpegMetadata',
                'add_chapters': True,
                'add_metadata': True,
            }, {
                'key': 'FFmpegSubtitlesConvertor',
                'format': 'srt'
            }, {
                'key': 'FFmpegThumbnailsConvertor',
                'format': 'jpg',
                # Run this before the actual video download
                'when': 'before_dl'
            }, {
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': True
            }, {
                'key': 'FFmpegEmbedSubtitle'
            }

            ],
            'outtmpl': '.' + getenv('ouputformat'),
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            self.status_msg = self.update.message.reply_text('Downloading...', quote=True)
            pprint.pprint(opts)
            try:
                ydl.download([url])
                self.telegram_bot.edit_message(self.status_msg, f"Download Completed")
            except Exception as ex:
                self.telegram_bot.edit_message(self.status_msg, f'Unexpected error occurred: {ex=}')
                print(f"Unexpected error occurred: {ex=}", flush=True)


class MyLogger(object):

    def __init__(self, telegram_bot: Telegram):
        self.telegram_bot = telegram_bot

    def debug(self, msg):
        print("debug: " + msg)
        pass

    def warning(self, msg):
        print("warning: " + msg)
        pass

    def error(self, msg):
        self.telegram_bot.send_message(msg)


def main():
    print("App started v0.01", flush=True)

    for env in ["tgtoken", "tgchatid", "ytdldir"]:
        if env not in environ:
            print(env + ' not found', flush=True)
            exit(1)
    del env

    telegram_bot = Telegram(getenv('tgtoken'), int(getenv('tgchatid')))
    telegram_bot.send_message("Ready")
    telegram_bot.start_polling()


if __name__ == '__main__':
    main()
