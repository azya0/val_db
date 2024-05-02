from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.engine import get_async_session
from db.models import Detail, DetailType, Model, Order_xref_Detail, Work
from routers.schemas import DetailScheme, DetailSchemeRead, DetailTypeScheme, WorkScheme, WorkSchemeRead


router = APIRouter(
    prefix="/services",
    tags=["services"],
)


@router.post('/detail/type', name="Добавляет тип детали для автомобиля", response_model=DetailTypeScheme)
async def post_detail_type(name: str, session: AsyncSession = Depends(get_async_session)):
    detail_type = DetailType(name=name)

    session.add(detail_type)
    await session.commit()
    await session.refresh(detail_type)

    return detail_type


@router.get('/detail/types', name="Выводит список типов деталей автомобиля", response_model=list[DetailTypeScheme])
async def get_detail_types(session: AsyncSession = Depends(get_async_session)):
    return (await session.scalars(select(DetailType))).all()


@router.delete('/detail/type/{id}', name="Удаляет тип детали автомобился по ID")
async def post_detail_type(id: int, session: AsyncSession = Depends(get_async_session)):
    to_delete = await session.get(DetailType, id)

    if to_delete is None:
        raise HTTPException(404, 'no detail type with such id')
    
    await session.delete(to_delete)


@router.post('/detail', name="Добавляет деталь определенного типа", response_model=DetailScheme)
async def post_detail(data: DetailSchemeRead, session: AsyncSession = Depends(get_async_session)):
    model = await session.get(Model, data.model_id)

    if model is None:
        raise HTTPException(404, 'wrong model id')
    
    detail_type = await session.get(DetailType, data.type_id)

    if detail_type is None:
        raise HTTPException(404, 'wrong detail_type id')

    result = Detail(**data.model_dump())

    session.add(result)
    await session.commit()
    await session.refresh(result)

    result.model = model
    result.detail_type = detail_type

    return result


@router.get('/details', name="Выводит список имеющихся деталей", response_model=list[DetailScheme])
async def get_details(session: AsyncSession = Depends(get_async_session)):
    requrst = select(Detail).filter(~Detail.id.in_(select(Order_xref_Detail.detail_id)))
    return (await session.scalars(requrst.options(selectinload(Detail.model), selectinload(Detail.detail_type), ))).all()



@router.post('/work', name="Добавляет вид работы", response_model=WorkScheme)
async def post_work(data: WorkSchemeRead, session: AsyncSession = Depends(get_async_session)):
    work = Work(**data.model_dump())

    session.add(work)
    await session.commit()
    await session.refresh(work)

    return work


@router.get('/works', name="Выводит список видов работ", response_model=list[WorkScheme])
async def get_works(session: AsyncSession = Depends(get_async_session)):
    return (await session.scalars(select(Work))).all()


@router.delete('/work/{id}', name="Удаляет вид работы по ID")
async def delete_work(id: int, session: AsyncSession = Depends(get_async_session)):
    work = await session.get(Work, id)

    if work is None:
        raise HTTPException(404, 'no work with such id')
    
    await session.delete(work)
