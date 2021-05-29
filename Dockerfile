FROM debian:latest
RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y
RUN pip3 install -U pip
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm
RUN git clone https://iam-pro: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@github.com/iam-pro/vcbot.git
WORKDIR vcbot
RUN pip3 install -r requirements.txt
CMD python3 main.py
