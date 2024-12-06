from http import HTTPStatus

from fastapi import FastAPI

from todo_list.routers import auth, html_example, users
from todo_list.schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(html_example.router)


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


# parei no minuto 26:15 da live
