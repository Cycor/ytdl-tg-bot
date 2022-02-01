#!/bin/sh
cd "$(dirname "$0")"

docker buildx build --platform linux/amd64 -t cycor/ytdl-tg-bot:latest -o type=docker .
