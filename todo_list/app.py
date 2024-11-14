from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from todo_list.schemas import Message

app = FastAPI()


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
