import os
import shutil
from fastapi import FastAPI, exceptions
from app_types import ModelRequest, ModelResponse, CarDefect, CarDefectType


UPLOAD_DIR = "static/uploads"
PROCESSED_DIR = "static/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/check_car")
async def check_car(request: ModelRequest) -> ModelResponse:
    for filename in request.files:
        src_path = os.path.join(UPLOAD_DIR, filename)
        dst_path = os.path.join(PROCESSED_DIR, filename)

        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
        else:
            raise exceptions.HTTPException(status_code=404, detail="Item not found")

    response = ModelResponse(
        files=request.files,
        defects=[
            CarDefect(type=CarDefectType(0), area=5.)
        ]
    )
    return response
