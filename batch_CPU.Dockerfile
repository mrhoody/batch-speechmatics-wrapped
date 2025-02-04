FROM python:3.12.8-alpine3.20
# TODO: replace with speechmatics on-prem container as base
# FROM batch-asr-transcriber-en:11.0.1

# set working directory, but according to speechmatics it can work from root
# WORKDIR /opt/orchestrator

# TODO: add python to speechmatics on-prem container
RUN apt-get update
RUN apt-get install -y python3 --no-cache-dir

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./config.json .
COPY ./main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]