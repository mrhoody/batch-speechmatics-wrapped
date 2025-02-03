FROM python:3.12.8-alpine3.20
# TODO: replace with speechmatics on-prem container as base
# FROM batch-asr-transcriber-en:11.0.1

WORKDIR /opt/orchestrator

# TODO: add python to speechmatics on-prem container

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]