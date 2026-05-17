import pytest
from helpers.courier_helpers import (
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier,
)


@pytest.fixture
def new_courier():
    """
    Регистрирует курьера и логинится, чтобы получить id.
    Возвращает словарь {'login': ..., 'password': ..., 'firstName': ..., 'id': ...}.
    """
    creds = register_new_courier_and_return_login_password()
    login, password, first_name = creds
    courier_id = login_courier(login, password).json().get("id")

    yield {"login": login, "password": password, "firstName": first_name, "id": courier_id}

    delete_courier(courier_id)


@pytest.fixture
def registered_courier_id(new_courier):
    """
    Возвращает id уже зарегистрированного курьера.
    """
    return new_courier["id"]


@pytest.fixture
def courier_cleaner():
    """
    Фикстура для очистки курьера, созданного внутри теста.
    """
    data = {}
    yield data
    if data:
        courier_id = login_courier(data["login"], data["password"]).json().get("id")
        delete_courier(courier_id)