from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from todo_list.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()
fake_db = []  # apenas para testes iniciais do projeto


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/hello-world', response_class=HTMLResponse)
def hello_world():
    return """
    <html>
      <head>
        <title> Our Hello World!</title>
      </head>
      <body>
        <h1> Hello World! </h1>
      </body>
    </html>"""


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        id=len(fake_db) + 1,
        **user.model_dump(),  # converte o schema em um dict e desempacota as chaves e valores
    )
    fake_db.append(user_with_id)
    return user_with_id


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int):
    if user_id < 1 or user_id > len(fake_db):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return fake_db[user_id - 1]


@app.get('/users/', response_model=UserList)
def get_users():
    return {'users': fake_db}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(fake_db):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    fake_db[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(fake_db):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    del fake_db[user_id - 1]
    return {'message': 'User deleted'}
