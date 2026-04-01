from sqlalchemy import select, update, delete
from database.models import async_session, User, Service, Order
from sqlalchemy.orm import selectinload
from sqlalchemy import or_, and_


# User
async def get_user(tg_id: int):
    async with async_session() as s:
        user = await s.scalar(select(User).where(User.tg_id == tg_id))
        return user

async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users.all()

async def get_user_by_id(user_id: int):
    async with async_session() as s:
        user = await s.scalar(select(User).where(User.id == user_id))
        return user
async def create_user(tg_id: int, role: str, name: str):
    async with async_session() as session:
        new_user = User(
            tg_id=tg_id,
            role=role,
            name=name
        )
        session.add(new_user)
        await session.commit()
        return new_user
async def update_user_role(user_id, role):
    async with async_session() as session:
        await session.execute(update(User).where(User.id == user_id).values(role=role))
        await session.commit()

# Service
async def create_service(user_id, title, description, price):
    async with async_session() as session:
        new_service = Service(
            user_id=user_id,
            title=title,
            description=description,
            price=price
        )
        session.add(new_service)
        await session.commit()
        return new_service

async def get_all_services():
    async with async_session() as session:
        # Получаем все услуги
        result = await session.scalars(select(Service))
        services = result.all()

        # Для каждой услуги вручную подгружаем пользователя
        for service in services:
            # Подгружаем пользователя по user_id
            user_result = await session.scalars(
                select(User).where(User.id == service.user_id)
            )
            service.user = user_result.first()  # 👈 прикрепляем пользователя к услуге

        return services
async def get_user_services(user_id):
    async with async_session() as session:
        user = await session.scalars(select(Service).where(Service.user_id == user_id))
        return user.all()

async def get_service(service_id):
    async with async_session() as session:
        service = await session.scalar(select(Service).where(Service.id == service_id))
        return service
async def update_service(service_id, title, description, price):
    async with async_session() as session:
        await session.execute(update(Service).where(Service.id == service_id).values(title=title, description=description, price=price))
        await session.commit()
async def delete_service(service_id):
    async with async_session() as session:
        await session.execute(delete(Order).where(Order.service_id == service_id))
        await session.execute(delete(Service).where(Service.id == service_id))
        await session.commit()

# Order
async def create_order(client_id, executor_id, service_id, comment):
    async with async_session() as session:
        new_order = Order(
            client_id=client_id,
            executor_id=executor_id,
            service_id=service_id,
            comment=comment
        )
        session.add(new_order)
        await session.commit()
        # 👇 Добавь эту строку! Она загружает свежие данные объекта из БД
        await session.refresh(new_order)
        # 👇 Теперь можно безопасно вернуть ID
        return new_order.id

async def get_client_orders(client_id):
    async with async_session() as session:
        order = await session.scalars(select(Order).where(Order.client_id == client_id))
        return order.all()

async def get_executor_orders(executor_id):
    async with async_session() as session:
        order = await session.scalars(select(Order).where(Order.executor_id == executor_id))
        return order.all()
async def get_order(order_id):
    async with async_session() as session:
        order = await session.scalar(select(Order).where(Order.id == order_id))
        return order
async def update_order_status(order_id, new_status):
    async with async_session() as session:
        await session.execute(update(Order).where(Order.id == order_id).values(status=new_status))
        await session.commit()
async def get_orders():
    async with async_session() as session:
        orders = await session.scalars(select(Order))
        return orders.all()
async def get_orders_by_status(status, user_id):
    async with async_session() as session:
        orders = await session.scalars(select(Order).where(and_(or_(Order.executor_id == user_id, Order.client_id == user_id), Order.status == status)))
        return orders.all()
