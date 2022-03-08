# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN chmod +x gunicorn.sh 

#CMD [ "python3", "app.py" ]
CMD ["sh", "gunicorn.sh"]

