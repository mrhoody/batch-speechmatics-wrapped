import subprocess
import os
import json

from fastapi import FastAPI, File, UploadFile, status

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
    if File.content_type != "audio/wav":
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "invalid file uploaded, only .wav files are accepted",
        }
    try:
        # Save the uploaded file as input.audio as speechmatics requirements
        with open("/input.audio", "wb") as f:  # default to root directory for now
            f.write(File.file.read())

        # Run the docker container with the input file
        run_command = ["pipeline"]
        result = subprocess.run(run_command, stdout=subprocess.PIPE).stdout.decode(
            "utf-8"
        )

        # Convert stdout result to dictionary
        processed_result = json.loads(result)

        # Clear the input file
        os.remove("/input.audio")
        return {
            "status": status.HTTP_200_OK,
            "filename": File.filename,
            "message": "transcription generated successfully",
            "results": processed_result["results"],
        }
    except Exception as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"file transcription failed due to the following: {e}",
        }
