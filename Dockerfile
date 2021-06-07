FROM programmingerror/ultroid:v0.0.2
RUN git clone https://github.com/iam-pro/vcbot.git
WORKDIR vcbot
RUN pip3 install -r requirements.txt
CMD python3 main.py
