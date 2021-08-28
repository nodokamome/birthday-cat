FROM python:3.7.9

WORKDIR /usr/src/app

COPY app/ /usr/src/app

CMD pip install --no-cache-dir -r requirements.txt && python src/main.py
