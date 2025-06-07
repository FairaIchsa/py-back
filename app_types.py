import pydantic
import enum


class ModelRequest(pydantic.BaseModel):
    images: list[str]


class CarDefectType(enum.Enum):
    missing_part = 0    # Отсутствующая деталь
    broken_part = 1     # Сломанная деталь
    scratch = 2         # Царапина
    cracked = 3         # Трещина
    dent = 4            # Вмятина
    flaking = 5         # Отслоение покрытия
    paint_chip = 6      # Скол краски
    corrosion = 7       # Коррозия

    def __str__(self):
        return self.name


class CarDefect(pydantic.BaseModel):
    class Config:
        json_encoders = {CarDefectType: lambda t: t.name}

    type: CarDefectType
    area: float


class ModelResponse(pydantic.BaseModel):
    defects: list[CarDefect]
    images: list[str]
