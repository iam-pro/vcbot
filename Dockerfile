FROM programmingerror/ultroid:v0.0.2
RUN git clone https://iam-pro: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@github.com/iam-pro/vcbot.git
WORKDIR vcbot
RUN pip3 install -r requirements.txt
RUN git pull
CMD python3 main.py
