FROM python3.10-nodejs17-bullseye
COPY . .
RUN pip3 install -r requirements.txt
CMD python3 main.py
