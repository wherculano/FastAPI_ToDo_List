from http import HTTPStatus


def test_deve_retornar_hello_world_e_ok(client):
    response = client.get('/html/hello-world')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Hello World! </h1>' in response.text
