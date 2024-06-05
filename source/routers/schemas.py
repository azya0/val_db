import datetime
from pydantic import BaseModel


class ID:
    id: int


class DetailTypeScheme(BaseModel, ID):
    name: str

    class Config:
        from_attributes = True


class DetailSchemeRead(BaseModel):
    cost: float
    type_id: int
    model_id: int
    name: str


class ModelScheme(BaseModel, ID):
    name: str

    class Config:
        from_attributes = True


class DetailScheme(DetailSchemeRead, ID):
    model: ModelScheme
    detail_type: DetailTypeScheme

    class Config:
        from_attributes = True


class CarScheme(BaseModel, ID):
    model_id: int
    model: ModelScheme

    class Config:
        from_attributes = True


class ClientSchemeRead(BaseModel):
    first_name: str 
    second_name: str
    patronymic: str | None = None

    car_models: list[int]


class ClientScheme(BaseModel, ID):
    first_name: str 
    second_name: str
    patronymic: str | None = None

    cars: list[CarScheme]


class ClientSchemeShort(BaseModel, ID):
    first_name: str 
    second_name: str
    patronymic: str | None = None

    class Config:
        from_attributes = True



class WorkSchemeRead(BaseModel):
    cost: float
    time_cost: datetime.datetime
    name: str


class WorkScheme(WorkSchemeRead, ID):
    class Config:
        from_attributes = True


class OrderNewReadScheme(BaseModel):
    first_name: str 
    second_name: str
    patronymic: str | None = None

    model_id: int

    details_id: list[int] | None = None
    works_id: list[int] | None = None


class OrderSchemeRead(BaseModel):
    details_id: list[int] | None = None
    works_id: list[int] | None = None


class OrderScheme(BaseModel, ID):
    total: float
    
    client: ClientSchemeShort
    car: CarScheme
    details: list[DetailScheme]
    works: list[WorkScheme]
    speedometer: float

    class Config:
        from_attributes = True


class OtchetScheme(BaseModel):
    total: float

    details: list[DetailScheme]
    works: list[WorkScheme]


class TestResults(BaseModel):
    test_name: str

    result_100000: int | None = None
    result_10000: int | None = None
    result_1000: int | None = None
