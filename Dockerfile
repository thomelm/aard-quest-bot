FROM python:3.11-slim

MAINTAINER "thomelm <thomas.e.elmer@gmail.com>"

COPY config.py ./
COPY discord_bot.py ./
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y telnet

CMD [ "python3", "./discord_bot.py" ]