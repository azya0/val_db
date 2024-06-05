from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_async_session
from db.models import Car, Client, Client_xref_Car, Model
from routers.car import post_car
from routers.schemas import CarScheme, ClientScheme, ClientSchemeRead


router = APIRouter(
    prefix="/client",
    tags=["client"],
)


@router.post('/client', name="Добавляет нового клиента СТО", response_model=ClientScheme)
async def post_client(data: ClientSchemeRead, session: AsyncSession = Depends(get_async_session)):
    models = []

    for model_id in data.car_models:
        model = await session.get(Model, model_id)

        if model is None:
            raise HTTPException(404, f'no model with id {model_id}')
        
        models.append(model)

    cars = []

    for model in models:
        car = await post_car(model.id, session)

        cars.append(car)
    
    client = Client(first_name=data.first_name, second_name=data.second_name, patronymic=data.patronymic)

    session.add(client)
    await session.commit()
    await session.refresh(client)

    for car in cars:
        session.add(Client_xref_Car(car_id=car.id, client_id=client.id))
    
    await session.commit()

    return ClientScheme(
        id=client.id,
        first_name=client.first_name,
        second_name=client.second_name,
        patronymic=client.patronymic,
        cars=cars
    )


@router.get('/client/{id}', name="Выводит данные о клиенте по ID", response_model=ClientScheme)
async def get_client(id: int, session: AsyncSession = Depends(get_async_session)):
    client = await session.get(Client, id, options=(selectinload(Client.cars), selectinload(Client.cars, Car.model), ))

    if client is None or not client.is_active:
        raise HTTPException(404, 'no client with such id')
    
    return client


@router.delete('/client/{id}', name="Удаляет данные о клиенте по ID")
async def delete_client(id: int, session: AsyncSession = Depends(get_async_session)):
    client = await session.get(Client, id, options=(selectinload(Client.cars), selectinload(Client.cars, Car.model), ))

    if client is None:
        raise HTTPException(404, 'no client with such id')

    for car in client.cars:
        car.is_active = False
        session.add(car)
    await session.commit()

    client.is_active = False
    session.add(client)
    await session.commit()


@router.post('/add/car', name="Добавляет автомобиль клиента по ID клиента и ID модели", response_model=CarScheme)
async def add_car(client_id: int, model_id: int, session: AsyncSession = Depends(get_async_session)):
    client = await session.get(Client, client_id)

    if client is None:
        raise HTTPException(404, 'no client with such id')
    
    model = await session.get(Model, model_id)

    if model is None:
        raise HTTPException(404, 'no model with such id')
    
    car = Car(model_id=model_id)

    session.add(car)
    await session.commit()
    await session.refresh(car)

    session.add(Client_xref_Car(car_id=car.id, client_id=client.id))
    await session.commit()

    car.model = model

    return car


@router.get('/clients', name="Выводит список клиентов СТО", response_model=list[ClientScheme])
async def get_clients(session: AsyncSession = Depends(get_async_session)):
    data = (await session.scalars(select(Client).filter(Client.is_active == True).options(selectinload(Client.cars), selectinload(Client.cars, Car.model)))).all()

    for client in data:
        new_cars = []
        for car in client.cars:
            if car.is_active:
                new_cars.append(car)
        client.cars = new_cars
    
    return data


@router.patch('/sellCar/{car_id}/{new_owner_id}', name="Передает автомобиль по id")
async def sellCar(car_id: int, new_owner_id: int, session: AsyncSession = Depends(get_async_session)):
    car = await session.get(Car, car_id)

    if car is None:
        raise HTTPException(404, detail="no such car")

    new_owner = await session.get(Client, new_owner_id)

    if new_owner is None:
        raise HTTPException(404, detail="no such client")
    
    old_connections = (await session.scalars(select(Client_xref_Car).where(Client_xref_Car.car_id == car_id))).all()

    for connection in old_connections:
        await session.delete(connection)
    
    new_connection = Client_xref_Car(car_id=car_id, client_id=new_owner_id)

    session.add(new_connection)
    await session.commit()
    