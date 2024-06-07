FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./
COPY ./data/* ./
COPY ./src/* ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./src/main.py" ]
