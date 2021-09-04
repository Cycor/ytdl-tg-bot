FROM python:3-alpine
LABEL org.opencontainers.image.source=https://github.com/emptyteeth/ytdl-tg-bot
ARG TARGETARCH
WORKDIR /
COPY bot.py .
RUN mkdir ytdl -m 777
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-${TARGETARCH}-static.tar.xz -q -O - | tar x -f - -J --strip 1 -C /usr/local/bin/
RUN pip install --no-cache-dir python-telegram-bot youtube-dl
USER nobody
ENV ytdldir=/ytdl
ENTRYPOINT ["/usr/local/bin/python", "bot.py"]
