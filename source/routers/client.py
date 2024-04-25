from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_async_session
from db.models import Car, Client, Client_xref_Car, Detail, Model, Work
from routers.car import post_car
from routers.schemas import CarScheme, ClientScheme, ClientSchemeRead, OrderNewReadScheme, OrderScheme


router = APIRouter(
    prefix="/client",
    tags=["client"],
)


@router.post('/client', response_model=ClientScheme)
async def post_client(data: ClientSchemeRead, session: AsyncSession = Depends(get_async_session)):
    if not len(data.car_models):
        raise HTTPException(400, 'no car models')
    
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


@router.get('/client/{id}', response_model=ClientScheme)
async def get_client(id: int, session: AsyncSession = Depends(get_async_session)):
    client = await session.get(Client, id, options=(selectinload(Client.cars), selectinload(Client.cars, Car.model), ))

    if client is None:
        raise HTTPException(404, 'no client with such id')
    
    return client


@router.delete('/client/{id}')
async def delete_client(id: int, session: AsyncSession = Depends(get_async_session)):
    client = await session.get(Client, id, options=(selectinload(Client.cars), selectinload(Client.cars, Car.model), ))

    if client is None:
        raise HTTPException(404, 'no client with such id')
    
    for xref in (await session.scalars(select(Client_xref_Car).where(Client_xref_Car.client_id == client.id))).all():
        await session.delete(xref)

    for car in client.cars:
        await session.delete(car)

    await session.delete(client)


@router.post('/add/car', response_model=CarScheme)
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


@router.get('/clients', response_model=list[ClientScheme])
async def get_clients(session: AsyncSession = Depends(get_async_session)):
    return (await session.scalars(select(Client).options(selectinload(Client.cars), selectinload(Client.cars, Car.model)))).all()


@router.post('/order/new_client', response_model=OrderScheme)
async def post_new_order(data: OrderNewReadScheme, session: AsyncSession = Depends(get_async_session)):
    cost = 0
    details = []

    for detail_id in data.details_id:
        detail = await session.get(Detail, detail_id, options=(selectinload(Detail.detail_type), selectinload(Detail.model)), )

        if detail is None:
            raise HTTPException(404, f'no detail with id {detail_id}')

        if detail.model.id != data.model_id:
            raise HTTPException(400, f'wrong car model for detail {detail_id}')

        cost += detail.cost
        details.append(detail)
    
    works = []

    for work_id in data.works_id:
        work = await session.get(Work, work_id)

        if work is None:
            raise HTTPException(404, f'no work with id {work_id}')
        
        cost += work.cost
        works.append(work)

    if not len(works) and not len(details):
        raise HTTPException(400, f'nothing selected')
    
    model = await session.get(Model, data.model_id)

    if model is None:
        raise HTTPException(404, 'wrong model id')

    car = Car(model_id=model.id)

    session.add(car)
    await session.commit()
    await session.refresh(car)

    car.model = model

    client = Client(
        first_name=data.first_name,
        second_name=data.second_name,
        patronymic=data.patronymic,
    )

    session.add(client)
    await session.commit()
    await session.refresh(client)

    xref = Client_xref_Car(client_id=client.id, car_id=car.id)

    session.add(xref)
    await session.commit()
    await session.refresh(xref)

    return OrderScheme(
        total=cost,
        car=car,
        details=details,
        works=works,
    )


# @router.post('/order', response_model=OrderScheme)
# async def post_order()