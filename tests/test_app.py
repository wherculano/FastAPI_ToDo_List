from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_deve_retornar_hello_world_e_ok(client):
    response = client.get('/hello-world')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Hello World! </h1>' in response.text


def test_create_user(client):
    response = client.post('/users/', json={'username': 'Wagner', 'email': 'wag@herculano.com', 'password': '12334'})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'Wagner', 'email': 'wag@herculano.com', 'id': 1}


def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'Wagner', 'email': 'wag@herculano.com', 'id': 1}


def test_get_user_not_found(client):
    response = client.get('/users/10')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    # erroneamente, este teste depende do teste anterior (que cadastra o user)
    assert response.json() == {'users': [{'username': 'Wagner', 'email': 'wag@herculano.com', 'id': 1}]}


def test_update_user(client):
    response = client.put(
        '/users/1', json={'username': 'WagHerculano', 'email': 'wag@herculano.com', 'password': '12334'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'WagHerculano', 'email': 'wag@herculano.com', 'id': 1}


def test_update_user_not_found(client):
    response = client.put('/users/10', json={'username': 'Pizza', 'email': 'pizza@lover.com', 'password': '123'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/10')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
