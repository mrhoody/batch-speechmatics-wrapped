FROM speechmatics-docker-demo.jfrog.io/sm-gpu-transcriber-batch-en-singapore_poc

# TODO: add python to speechmatics on-prem container
RUN apt-get update
RUN apt-get install -y python3.12

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "fastapi[standard]"

COPY ./config.json /config.json
# COPY ./license.json /license.json
COPY ./main.py .

EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "main.py", "--port", "8000"]