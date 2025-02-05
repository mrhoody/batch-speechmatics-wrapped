import subprocess
import os
import json

from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/list_files")
def list_files():
    result = subprocess.run(["ls"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    return {"stdout": result}


@app.post("/speechmatics_batch_wrapper")
def speechmatics_batch_wrapper(file: UploadFile = File(...)) -> JSONResponse:
    if file.content_type != "audio/wav":
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "invalid file uploaded, only .wav files are accepted",
        }
    # TODO: Add a check for the file size (< 4GB per https://docs.speechmatics.com/on-prem/containers/cpu-container#batch-transcription)
    # TODO: Add a check for the file duration (< 2 hours per https://docs.speechmatics.com/on-prem/containers/cpu-container#batch-transcription)
    try:
        # Save the uploaded file to /input.audio as speechmatics requirements
        with open("/input.audio", "wb") as f:  # default to root directory for now
            f.write(file.file.read())

        # Run the docker container with the input file
        run_command = ["pipeline"]
        result = subprocess.run(run_command, stdout=subprocess.PIPE).stdout.decode(
            "utf-8"
        )  # exit code == 0 is success, exit code != 0 is failure with stack trace

        # Convert stdout result to dictionary
        processed_result = json.loads(result)

        # Clear the input file for next job
        os.remove("/input.audio")

        # Return the results
        return {
            "status": status.HTTP_200_OK,
            "filename": file.filename,
            "message": "transcription generated successfully",
            "results": processed_result["results"],
        }
    except Exception as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"file transcription failed due to the following: {e}",
        }
