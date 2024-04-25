from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_async_session
from db.models import Car, Model
from routers.schemas import CarScheme, ModelScheme


router = APIRouter(
    prefix="/car",
    tags=["car"],
)


@router.post('/model', response_model=ModelScheme)
async def post_detail_type(name: str, session: AsyncSession = Depends(get_async_session)):
    model = Model(name=name)

    session.add(model)
    await session.commit()
    await session.refresh(model)

    return model


@router.get('/models', response_model=list[ModelScheme])
async def get_detail_types(session: AsyncSession = Depends(get_async_session)):
    return (await session.scalars(select(Model))).all()


@router.delete('/model/{id}')
async def post_detail_type(id: int, session: AsyncSession = Depends(get_async_session)):
    to_delete = await session.get(Model, id)

    if to_delete is None:
        raise HTTPException(404, 'no model with such id')
    
    await session.delete(to_delete)


@router.post('/car', response_model=CarScheme)
async def post_car(model_id: int, session: AsyncSession = Depends(get_async_session)):
    model = await session.get(Model, model_id)

    if model is None:
        raise HTTPException(404, 'wrong model id')
    
    car = Car(model_id=model_id)

    session.add(car)
    await session.commit()
    await session.refresh(car)

    car.model = model
    
    return car


@router.get('/cars', response_model=list[CarScheme])
async def get_cars(session: AsyncSession = Depends(get_async_session)):
    return (await session.scalars(select(Car).options(selectinload(Car.model), ))).all()
