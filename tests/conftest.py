import pytest
from helpers.courier_helpers import (
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier,
)


@pytest.fixture
def new_courier():
    """
    Регистрирует курьера перед тестом и удаляет его после.
    Возвращает словарь {'login': ..., 'password': ..., 'firstName': ...}.
    """
    creds = register_new_courier_and_return_login_password()
    assert creds, "Не удалось зарегистрировать курьера"
    login, password, first_name = creds

    yield {"login": login, "password": password, "firstName": first_name}

    response = login_courier(login, password)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            delete_courier(courier_id)
