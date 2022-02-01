FROM python:3
LABEL org.opencontainers.image.source=https://github.com/emptyteeth/ytdl-tg-bot
ARG TARGETARCH

RUN apt-get clean && apt-get -y update && apt-get -y install --no-install-recommends \
    build-essential \
    gcc \
    curl && rm -rf /var/lib/apt/lists/*

# FFmpeg
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-${TARGETARCH}-static.tar.xz -q -O - | tar x -f - -J --strip 1 -C /usr/local/bin/
	
WORKDIR /app
COPY requirements.txt .

# Dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

RUN mkdir /ytdl -m 777
RUN mkdir /.cache -m 777
RUN mkdir /.cache/yt-dlp -m 777

ENV ytdldir=/ytdl
ENV format='best'
ENV ouputformat='/%(title)s-%(id)s.%(ext)s'

CMD ["python", "-u", "bot.py"]
