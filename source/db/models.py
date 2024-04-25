import datetime

from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import as_declarative, relationship


@as_declarative()
class Base:
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)


@as_declarative()
class Human:
    first_name = Column(String(64), nullable=False)
    second_name = Column(String(64), nullable=False)
    patronymic = Column(String(64), nullable=True)


class Detail(Base):
    __tablename__ = 'detail'

    cost = Column(Float, default=0.0)
    type_id = Column(Integer, ForeignKey('detail_type.id'), nullable=False)
    model_id = Column(Integer, ForeignKey('model.id'), default=None, nullable=True)
    name = Column(String(128), nullable=False)

    detail_type = relationship("DetailType", back_populates="details", uselist=False)
    model = relationship("Model", back_populates="details", uselist=False)


class DetailType(Base):
    __tablename__ = 'detail_type'
    
    name = Column(String(128), nullable=False, unique=True)

    details = relationship("Detail", back_populates='detail_type')


class Model(Base):
    __tablename__ = 'model'

    name = Column(String(128), nullable=False)

    details = relationship("Detail", back_populates="model")
    cars = relationship("Car", back_populates="model")


class Car(Base):
    __tablename__ = 'car'

    model_id = Column(Integer, ForeignKey('model.id'), nullable=False)

    model = relationship("Model", back_populates="cars", uselist=False)
    client = relationship("Client", secondary='client_xref_car', back_populates='cars', uselist=False)


class Client(Base, Human):
    __tablename__ = 'client'

    cars = relationship("Car", secondary='client_xref_car', back_populates='client')


class Client_xref_Car(Base):
    __tablename__ = 'client_xref_car'

    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('car.id'), nullable=False)


class Work(Base):
    __tablename__ = 'work'

    cost = Column(Float, default=0.0)
    time_cost = Column(DateTime, nullable=False)
    name = Column(String(128), nullable=False)


class Order(Base):
    __tablename__ = 'order'

    car_id = Column(Integer, ForeignKey('car.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    speedometer = Column(Float, default=0.0)


class Order_xref_Detail(Base):
    __tablename__ = 'order_xref_detail'

    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    detail_id = Column(Integer, ForeignKey('detail.id'), nullable=False)


class Order_xref_Work(Base):
    __tablename__ = 'order_xref_work'

    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    work_id = Column(Integer, ForeignKey('work.id'), nullable=False)
