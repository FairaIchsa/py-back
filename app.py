from fastapi import FastAPI
import base64

from app_types import ModelRequest, ModelResponse, CarDefect, CarDefectType


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/check_car")
async def check_car(request: ModelRequest) -> ModelResponse:
    response = ModelResponse(
        images=request.images,
        defects=[
            CarDefect(type=CarDefectType(0), area=5.)
        ]
    )
    return response
