from http import HTTPStatus

from fast_zero.schemas import UserPublicSchema


def test_root_deve_retornar_ok_e_welcome(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to the FastAPI application!'}


def test_exercicios_status_deve_retornar_ok_e_working(client):
    response = client.get('/status')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> API Working </h1>' in response.text


def test_post_user(client):
    response = client.post(
        '/users', json={'username': 'testuser', 'email': 'test@email.com', 'password': 'testpassword'}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'username': 'testuser', 'email': 'test@email.com'}


def test_show_user(client):
    response = client.get('/user/1')
    assert response.status_code == HTTPStatus.OK
    # Valida se o JSON da resposta é compatível com o esquema
    user_data = response.json()
    validated_user = UserPublicSchema(**user_data)
    assert validated_user.model_dump() == user_data  # Use model_dump() em vez de dict()


def test_fail_show_user(client):
    response = client.get('/user/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_list_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{'id': 1, 'username': 'testuser', 'email': 'test@email.com'}]}


def test_update_user(client):
    response = client.put(
        '/user/1', json={'id': 1, 'username': 'newtestuser', 'email': 'test@email.com', 'password': 'testpassword'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'username': 'newtestuser', 'email': 'test@email.com'}


def test_fail_update_user(client):
    response = client.put('/user/999', json={'username': 'newtestuser'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_fail_delete_user(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
