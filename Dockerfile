FROM nikolaik/python-nodejs:python3.9-nodejs16
COPY . .
RUN pip3 install -r requirements.txt
CMD python3 main.py
