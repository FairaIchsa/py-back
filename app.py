import os
from ultralytics import YOLO
from fastapi import FastAPI, exceptions
from app_types import ModelRequest, ModelResponse, CarDefect, CarDefectType, ImageResult


UPLOAD_DIR = "static/uploads"
PROCESSED_DIR = "static/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

damage_detection_model = YOLO("ml_models/damage_detection_model.pt")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/check_car")
async def check_car(request: ModelRequest) -> ModelResponse:
    image_results: list[ImageResult] = []

    for filename in request.files:
        defects: list[CarDefect] = []

        src_path = os.path.join(UPLOAD_DIR, filename)
        # dst_path = os.path.join(PROCESSED_DIR, filename)

        if os.path.exists(src_path):
            results = damage_detection_model.predict(
                source=src_path,  # путь к тестовым изображениям
                save=True,  # сохранять результаты с разметкой
                imgsz=640,  # размер изображения (должен совпадать с обучением)
                conf=0.65,  # порог уверенности (можно взять из inference_config.yaml)
                iou=0.5,  # порог IoU
                project=PROCESSED_DIR.split('/')[0],
                name=PROCESSED_DIR.split('/', 1)[1],
                exist_ok=True
            )

            for result in results:
                defects.append(
                    CarDefect(
                        type=CarDefectType(result.summary()[0]['class']),
                        polygon=list(*result.masks.xyn)
                    )
                )
            image_results.append(ImageResult(
                filename=filename,
                defects=defects
            ))
        else:
            raise exceptions.HTTPException(status_code=404, detail="Item not found")

    response = ModelResponse(
        result=image_results
    )
    return response
