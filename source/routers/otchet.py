from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.engine import get_async_session
from db.models import Car, Client, Detail, Order_xref_Detail, Order_xref_Work, Work
from routers.schemas import OtchetScheme


router = APIRouter(
    prefix="/otchet",
    tags=["otchet"],
)


@router.get('/all', name="Выводит отчет по продажам")
async def get_otchet(session: AsyncSession = Depends(get_async_session)):
    total = 0

    pre_details = (await session.scalars(select(Order_xref_Detail))).all()
    pre_works = (await session.scalars(select(Order_xref_Work))).all()

    details = []

    for pre_detail in pre_details:
        detail = await session.get(Detail, pre_detail.detail_id, options=(selectinload(Detail.detail_type), selectinload(Detail.model), ))

        total += detail.cost
        details.append(detail)
    
    works = []

    for pre_work in pre_works:
        work = await session.get(Work, pre_work.work_id)

        total += work.cost
        works.append(work)
    
    return OtchetScheme(
        total=total,
        details=details,
        works=works,
    )


@router.get('/mail', name="Формирует письмо для клиента с напоминанием")
async def get_mail(client_id: int, car_id: int, session: AsyncSession = Depends(get_async_session)):
    client = await session.get(Client, client_id)

    if client is None:
        raise HTTPException(404, 'wrong client id')
    
    car = await session.get(Car, car_id, options=(selectinload(Car.client), selectinload(Car.model), ))

    if car is None:
        raise HTTPException(404, 'wrong car id')
    
    if car.client != client:
        raise HTTPException(400, 'client have no such car')
    
    return f"Уважаемый {client.second_name} {client.first_name} {client.patronymic}, напоминаем вам о необходимости замены масла в вашем {car.model.name}!"
