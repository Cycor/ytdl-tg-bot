FROM python:3-alpine
LABEL org.opencontainers.image.source=https://github.com/emptyteeth/ytdl-tg-bot
ARG TARGETARCH
WORKDIR /
ENV ytdldir=/ytdl
COPY bot.py .
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-${TARGETARCH}-static.tar.xz -q -O - | tar x -f - -J --strip 1 -C /usr/local/bin/ && \
    pip install --no-cache-dir pyTelegramBotAPI youtube-dl && \
    mkdir ytdl && \
    adduser -D -H bot && \
    chown bot /ytdl
USER bot
ENTRYPOINT ["/usr/local/bin/python", "bot.py"]
