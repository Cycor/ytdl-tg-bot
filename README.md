# ytdl-tg-bot
a simple(rough) youtube-dl telegram bot

## Credits

- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

## Usage

- local
  - install package: ffmpeg
  - install pypi package: pyTelegramBotAPI youtube-dl
  - run:
  
    ```shell
    tgtoken="TG-BOT-TOKEN" tgchatid="TG-CHAT-ID" ytdldir="/PATH/TO/DOWNLOAD/DIR" python3 bot.py
    ```
  
- container

  ```shell
  docker run -d --restart=unless-stopped \
  -e tgtoken="TG-BOT-TOKEN" -e tgchatid="TG-CHAT-ID" \
  -v /PATH/TO/DOWNLOAD/DIR:/ytdl \
  ghcr.io/emptyteeth/ytdl-tg-bot:latest
  ```
