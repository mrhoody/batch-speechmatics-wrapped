import subprocess
import os

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# LICENSE_TOKEN = os.getenv("LICENSE_TOKEN")
# INPUT_FOLDER = os.getenv("INPUT_FOLDER") # commented out while we are using the root directory
# SM_INFERENCE_ENDPOINT=os.getenv("SM_INFERENCE_ENDPOINT") # commented out until we get to using GPU support

@app.get("/list_files")
def list_files():
    result = subprocess.run(["ls"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    return {"stdout": result}

@app.post("/speechmatics_batch_wrapper")
def speechmatics_batch_wrapper(File: UploadFile = File(...)):

    # Save the uploaded file as input.audio as speechmatics requirements
    with open("./input.audio", "wb") as f:  # default to root directory for now
        f.write(File.file.read())

    # Run the docker container with the input file
    run_command = [
        "pipeline"]
    result = subprocess.run(run_command, stdout=subprocess.PIPE).stdout.decode("utf-8")

    # Clear the input file
    os.remove("./input.audio")
    return {"stdout": result}
