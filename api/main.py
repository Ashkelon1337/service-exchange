from fastapi import FastAPI, HTTPException
import sys, os
from sqladmin import Admin, ModelView

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import database.requests as rq
from database.models import User, Service, Order, engine
import uvicorn


app = FastAPI(title='Service Exchange API')
admin = Admin(app, engine)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.tg_id, User.role, User.name] # колонки в списке
    column_searchable_list = [User.name] # по каким полям искать
    form_columns = [User.name, User.role] # поля для редактирования

class ServiceAdmin(ModelView, model=Service):
    column_list = [Service.id, Service.title, Service.price, Service.user_id]
    column_searchable_list = [Service.title]
    form_columns = [Service.title, Service.description, Service.price]

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.client_id, Order.executor_id, Order.status]
    column_searchable_list = [Order.id]
    form_columns = [Order.status]

admin.add_view(UserAdmin)
admin.add_view(ServiceAdmin)
admin.add_view(OrderAdmin)

@app.get('/')
async def root():
    return {'message': 'API работает'}

@app.get('/services')
async def get_services(): # Возвращает список всех услуг
    services = await rq.get_all_services()
    result = []
    for service in services:
        result.append({
            'id': service.id,
            'title': service.title,
            'description': service.description,
            'price': service.price,
            'user_id': service.user_id
        })
    return result

@app.get('/users')
async def get_users():
    users = await rq.get_users()
    if not users:
        raise HTTPException(status_code=404, detail='юзеров нет')
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'tg_id': user.tg_id,
            'role': user.role,
            'name': user.name
        })
    return result
@app.get('/services/{service_id}')
async def get_service(service_id: int):
    service = await rq.get_service(service_id)
    if not service:
        raise HTTPException(status_code=404, detail='Сервис с таким айди не найден!')
    return {
        'id': service.id,
        'title': service.title,
        'description': service.description,
        'price': service.price,
        'user_id': service.user_id
    }

@app.get('/users/{user_id}/services')
async def get_user_services(user_id: int):
    services = await rq.get_user_services(user_id)
    if not services:
        raise HTTPException(status_code=404, detail='Пользователь не найден!')
    result = []
    for service in services:
        result.append({
        'id': service.id,
        'title': service.title,
        'description': service.description,
        'price': service.price,
        'user_id': service.user_id
        })
    return result
if __name__ == '__main__':
    uvicorn.run('api.main:app', reload=True)