import requests
import random
import string
import allure

from urls import COURIER_URL, COURIER_LOGIN_URL


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_courier_payload():
    """Генерирует словарь с данными нового курьера."""
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10),
    }


@allure.step('Регистрируем нового курьера')
def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера. Возвращает [login, password, firstName] или []."""
    login_pass = []
    payload = generate_courier_payload()
    response = requests.post(COURIER_URL, data=payload)
    if response.status_code == 201:
        login_pass.append(payload["login"])
        login_pass.append(payload["password"])
        login_pass.append(payload["firstName"])
    return login_pass


@allure.step('Логинимся курьером с логином {login}')
def login_courier(login, password):
    """Выполняет логин курьера. Возвращает объект response."""
    payload = {"login": login, "password": password}
    return requests.post(COURIER_LOGIN_URL, data=payload)


@allure.step('Удаляем курьера с id {courier_id}')
def delete_courier(courier_id):
    """Удаляет курьера по id."""
    requests.delete(f'{COURIER_URL}/{courier_id}')