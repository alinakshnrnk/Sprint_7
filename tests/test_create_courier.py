import requests
import allure
from helpers.courier_helpers import (
    generate_random_string,
    generate_courier_payload,
)
from urls import COURIER_URL


@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Курьера можно создать')
    def test_create_courier_success(self, courier_cleaner):
        with allure.step('Генерируем данные нового курьера'):
            payload = generate_courier_payload()
            courier_cleaner.update(payload)

        with allure.step('Отправляем POST /courier'):
            response = requests.post(COURIER_URL, data=payload)

        with allure.step('Проверяем код ответа 201'):
            assert response.status_code == 201

    @allure.title('Успешный запрос возвращает ok: true')
    def test_create_courier_returns_ok_true(self, courier_cleaner):
        with allure.step('Генерируем данные нового курьера'):
            payload = generate_courier_payload()
            courier_cleaner.update(payload)

        with allure.step('Отправляем POST /courier'):
            response = requests.post(COURIER_URL, data=payload)

        with allure.step('Проверяем тело ответа {"ok": true}'):
            assert response.json() == {"ok": True}

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_cannot_create_duplicate_couriers(self, new_courier):
        with allure.step('Отправляем повторный запрос с теми же данными'):
            payload = {
                "login": new_courier["login"],
                "password": new_courier["password"],
                "firstName": new_courier["firstName"],
            }
            response = requests.post(COURIER_URL, data=payload)

        with allure.step('Проверяем код ответа 409'):
            assert response.status_code == 409

    @allure.title('Создание курьера с существующим логином возвращает ошибку')
    def test_duplicate_login_returns_error_message(self, new_courier):
        with allure.step('Отправляем запрос с уже существующим логином'):
            payload = {
                "login": new_courier["login"],
                "password": generate_random_string(10),
                "firstName": generate_random_string(10),
            }
            response = requests.post(COURIER_URL, data=payload)

        with allure.step('Проверяем код ответа 409 и сообщение об ошибке'):
            assert response.status_code == 409
            assert "логин уже используется" in response.json().get("message", "")

    @allure.title('Создание курьера без логина возвращает ошибку 400')
    def test_create_courier_without_login_returns_400(self):
        with allure.step('Отправляем запрос без поля login'):
            payload = generate_courier_payload()
            del payload["login"]
            response = requests.post(COURIER_URL, data=payload)

        with allure.step('Проверяем код ответа 400 и сообщение об ошибке'):
            assert response.status_code == 400
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи"

    @allure.title('Создание курьера без пароля возвращает ошибку 400')
    def test_create_courier_without_password_returns_400(self):
        with allure.step('Отправляем запрос без поля password'):
            payload = generate_courier_payload()
            del payload["password"]
            response = requests.post(COURIER_URL, data=payload)

        with allure.step('Проверяем код ответа 400 и сообщение об ошибке'):
            assert response.status_code == 400
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи"