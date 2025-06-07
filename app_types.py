import pydantic
import enum
import typing


class ModelRequest(pydantic.BaseModel):
    files: list[str]


CarDefectTypeSerializer = pydantic.PlainSerializer(
    lambda e: e.name,
    return_type='str',
    when_used='always'
)


class CarDefectType(enum.Enum):
    missing_part = 0    # Отсутствующая деталь
    broken_part = 1     # Сломанная деталь
    scratch = 2         # Царапина
    cracked = 3         # Трещина
    dent = 4            # Вмятина
    flaking = 5         # Отслоение покрытия
    paint_chip = 6      # Скол краски
    corrosion = 7       # Коррозия


class CarDefect(pydantic.BaseModel):
    type: typing.Annotated[CarDefectType, CarDefectTypeSerializer]
    area: float


class ModelResponse(pydantic.BaseModel):
    defects: list[CarDefect]
    files: list[str]
