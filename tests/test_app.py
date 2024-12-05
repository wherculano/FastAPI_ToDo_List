from http import HTTPStatus

from todo_list.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_deve_retornar_hello_world_e_ok(client):
    response = client.get('/hello-world')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Hello World! </h1>' in response.text


def test_create_user(client):
    response = client.post('/users/', json={'username': 'Wagner', 'email': 'test@test.com', 'password': 'password'})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'Wagner', 'email': 'test@test.com', 'id': 1}


def test_create_user_username_already_exists(client, user):
    response = client.post(
        '/users/', json={'username': user.username, 'email': 'xxxx@test.com', 'password': 'testtest'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exists(client, user):
    response = client.post('/users/', json={'username': 'Potatoes', 'email': user.email, 'password': 'testtest'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_get_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': user.username, 'email': user.email, 'id': user.id}


def test_get_user_not_found(client):
    response = client.get('/users/10')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1', json={'username': 'WagHerculano', 'email': 'test@test.com', 'password': 'password'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'WagHerculano', 'email': 'test@test.com', 'id': 1}


def test_update_user_not_found(client):
    response = client.put('/users/10', json={'username': 'Pizza', 'email': 'pizza@lover.com', 'password': '123'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/10')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
