FROM nikolaik/python-nodejs:python3.9-nodejs16
RUN git clone https://iam-pro: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@github.com/iam-pro/vcbot.git
WORKDIR vcbot
RUN pip3 install -r requirements.txt
CMD python3 main.py
