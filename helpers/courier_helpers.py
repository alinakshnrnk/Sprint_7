import requests
import random
import string
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@allure.step('Регистрируем нового курьера')
def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера. Возвращает [login, password, firstName] или []."""
    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }
    response = requests.post(f'{BASE_URL}/courier', data=payload)
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    return login_pass


@allure.step('Логинимся курьером с логином {login}')
def login_courier(login, password):
    """Выполняет логин курьера. Возвращает объект response."""
    payload = {"login": login, "password": password}
    return requests.post(f'{BASE_URL}/courier/login', data=payload)


@allure.step('Удаляем курьера с id {courier_id}')
def delete_courier(courier_id):
    """Удаляет курьера по id."""
    requests.delete(f'{BASE_URL}/courier/{courier_id}')