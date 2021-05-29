FROM nikolaik/python-nodejs
RUN pip3 install -r requirements.txt
CMD python3 main.py
