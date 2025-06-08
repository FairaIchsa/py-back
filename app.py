import os
from ultralytics import YOLO
import shutil
import cv2
import numpy as np
from PIL import Image
import time
from fastapi import FastAPI, exceptions
from app_types import ModelRequest, ModelResponse, CarDefect, CarDefectType, ImageResult


UPLOAD_DIR = "/Users/icetusk/Projects/ws-quiz/static/uploads"
PROCESSED_DIR = "/Users/icetusk/Projects/ws-quiz/static/processed"

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
        dst_path = os.path.join(PROCESSED_DIR, filename)

        if not os.path.exists(src_path):
            raise exceptions.HTTPException(status_code=404, detail=f"File {filename} not found")

        # ✅ Копируем файл
        shutil.copy(src_path, dst_path)

        # ✅ YOLO prediction
        results = damage_detection_model.predict(
            source=dst_path,
            save=False,
            imgsz=640,
            conf=0.65,
            iou=0.5,
            project=PROCESSED_DIR.split('/')[0],
            name=PROCESSED_DIR.split('/', 1)[1],
            exist_ok=True
        )

        # ✅ Загрузка изображения в OpenCV
        image = cv2.imread(dst_path)
        height, width = image.shape[:2]

        for result in results:
            masks = result.masks
            classes = result.boxes.cls.tolist() if result.boxes and result.boxes.cls is not None else []

            if masks and masks.xyn:
                for mask, class_id in zip(masks.xyn, classes):
                    # Сохраняем дефект
                    defects.append(
                        CarDefect(
                            type=CarDefectType(int(class_id)),
                            polygon=mask
                        )
                    )

                    # Рисуем на картинке
                    points = np.array([
                        [int(x * width), int(y * height)] for x, y in mask
                    ], dtype=np.int32)

                    cv2.polylines(image, [points], isClosed=True, color=(0, 0, 255), thickness=2)
                    cv2.fillPoly(image, [points], color=(0, 0, 255))

        # ✅ Сохраняем изображение с отрисованными повреждениями
        cv2.imwrite(dst_path, image)

        #time.sleep(5)

        image_results.append(ImageResult(
            filename=filename,
            defects=defects
        ))

    return ModelResponse(result=image_results)

