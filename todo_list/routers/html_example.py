from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix='/html', tags=['html'])


@router.get('/hello-world', response_class=HTMLResponse)
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
