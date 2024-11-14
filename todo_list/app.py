from http import HTTPStatus

from fastapi import FastAPI

from todo_list.schemas import Message

app = FastAPI()


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}
