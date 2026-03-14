from sqlalchemy import ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from datetime import datetime
from config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class User(Base): # Пользователи
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    role: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String(100))

class Service(Base): # Услуги
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(3333))
    price: Mapped[int] = mapped_column(Integer)

class Order(Base): # Заказы
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    executor_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id'))
    comment: Mapped[str] = mapped_column(String(3333))
    status: Mapped[str] = mapped_column(String, default='new')

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
