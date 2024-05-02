from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_async_session
from db.models import Car, Client, Client_xref_Car, Detail, Model, Order, Order_xref_Detail, Order_xref_Work, Work
from routers.schemas import OrderNewReadScheme, OrderScheme, OrderSchemeRead



router = APIRouter(
    prefix="",
    tags=["order"],
)


@router.post('/order/new_client', name="Добавляет заказ нового клиента СТО", response_model=OrderScheme)
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

    order = Order(car_id=car.id, client_id=client.id)
    
    session.add(order)
    await session.commit()
    await session.refresh(order)

    for detail in details:
        session.add(Order_xref_Detail(order_id=order.id, detail_id=detail.id))
    await session.commit()

    for work in works:
        session.add(Order_xref_Work(order_id=order.id, work_id=work.id))
    await session.commit()


    return OrderScheme(
        id=order.id,
        client=client,
        total=cost,
        car=car,
        details=details,
        works=works,
        speedometer=0,
    )


@router.post('/order', name="Добавляет заказ для старого-доброго клинета СТО", response_model=OrderScheme)
async def post_order(client_id: int, car_id: int, data: OrderSchemeRead, session: AsyncSession = Depends(get_async_session)):
    client = await session.get(Client, client_id)

    if client is None or not client.is_active:
        raise HTTPException(404, 'wrong client id')
    
    car = await session.get(Car, car_id, options=(selectinload(Car.client), selectinload(Car.model)))

    if car is None or not car.is_active:
        raise HTTPException(404, 'wrong car id')
    
    if car.client != client:
        raise HTTPException(400, 'client have no such car')
    
    cost = 0
    details = []

    for detail_id in data.details_id:
        detail = await session.get(Detail, detail_id, options=(selectinload(Detail.detail_type), selectinload(Detail.model)), )

        if detail is None:
            raise HTTPException(404, f'no detail with id {detail_id}')

        if detail.model.id != car.model_id:
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
    
    order = Order(car_id=car.id, client_id=client.id)
    
    session.add(order)
    await session.commit()
    await session.refresh(order)

    for detail in details:
        session.add(Order_xref_Detail(order_id=order.id, detail_id=detail.id))
    await session.commit()

    for work in works:
        session.add(Order_xref_Work(order_id=order.id, work_id=work.id))
    await session.commit()

    return OrderScheme(
        id=order.id,
        total=cost,
        car=car,
        client=client,
        details=details,
        works=works,
        speedometer=0,
    )


@router.get('/order/{id}', name="Выводит заказ по ID", response_model=OrderScheme)
async def get_order_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    order = await session.get(Order, id, options=(selectinload(Order.car), selectinload(Order.details), selectinload(Order.works), selectinload(Order.client),
                                                  selectinload(Order.car, Car.model), selectinload(Order.details, Detail.detail_type), selectinload(Order.details, Detail.model)))

    if order is None:
        raise HTTPException(404, 'wrong order id')
    
    total = 0

    for some in order.details + order.works:
        total += some.cost

    order.total = total

    return order


@router.patch('/speedometr', name="Выставляет показания спидометра заказу", response_model=OrderScheme)
async def patch_order(id: int, speedometr_data: float, session: AsyncSession = Depends(get_async_session)):
    order = await get_order_by_id(id, session)

    order.speedometer = speedometr_data

    return order


@router.get('/orders', name="Выводит список всех заказов", response_model=list[OrderScheme])
async def get_orders(session: AsyncSession = Depends(get_async_session)):
    ids = (await session.scalars(select(Order.id))).all()

    result = []

    for id in ids:
        result.append(await get_order_by_id(id, session))
    
    return result
