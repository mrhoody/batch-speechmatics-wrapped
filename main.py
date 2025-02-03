import subprocess
import os

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

TOKEN_VALUE = os.getenv("SPEECHMATICS_TOKEN")
CONTAINER_NAME = os.getenv("SPEECHMATICS_CONTAINER_NAME")
INPUT_FOLDER = os.getenv("INPUT_FOLDER")


@app.post("/speechmatics_batch_wrapper")
def speechmatics_batch_wrapper(File: UploadFile = File(...)):

    # Save the uploaded file as input.audio as speechmatics requirements
    with open(f"~/{INPUT_FOLDER}/input.audio", "wb") as f:
        f.write(File.file.read())

    # Run the docker container with the input file
    run_command = [
        "docker",
        "run",
        "-i",
        "-v",
        f"~/{INPUT_FOLDER}:/input.audio",
        "-e",
        f"LICENSE_TOKEN={TOKEN_VALUE}",
        f"{CONTAINER_NAME}",
    ]

    # TODO: use actual command from speechmatics pipeline CLI
    # result = subprocess.run("ls", stdout=subprocess.PIPE).stdout.decode("utf-8")

    result = subprocess.run(run_command, stdout=subprocess.PIPE).stdout.decode(
        "utf-8"
    )  # placeholder command
    return {"stdout": result}
