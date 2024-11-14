from http import HTTPStatus

from fastapi.testclient import TestClient

from todo_list.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_deve_retornar_hello_world_e_ok():
    client = TestClient(app)
    response = client.get('/hello-world')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Hello World! </h1>' in response.text
