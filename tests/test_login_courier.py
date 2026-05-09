import requests
import allure
from helpers.courier_helpers import (
    BASE_URL,
    generate_random_string,
    login_courier,
)


@allure.feature('Логин курьера')
class TestCourierLogin:

    @allure.title('Курьер может авторизоваться')
    def test_courier_can_login(self, new_courier):
        with allure.step('Отправляем POST /courier/login с корректными данными'):
            response = login_courier(new_courier["login"], new_courier["password"])

        with allure.step('Проверяем код ответа 200'):
            assert response.status_code == 200

    @allure.title('Успешный логин возвращает id курьера')
    def test_successful_login_returns_id(self, new_courier):
        with allure.step('Отправляем POST /courier/login'):
            response = login_courier(new_courier["login"], new_courier["password"])

        with allure.step('Проверяем наличие id в теле ответа'):
            assert "id" in response.json()
            assert response.json()["id"] is not None

    @allure.title('Логин без поля login возвращает ошибку 400')
    def test_login_without_login_field_returns_400(self):
        with allure.step('Отправляем запрос без поля login'):
            payload = {"password": generate_random_string(10)}
            response = requests.post(f'{BASE_URL}/courier/login', data=payload)

        with allure.step('Проверяем код ответа 400'):
            assert response.status_code == 400

    @allure.title('Логин без поля password возвращает ошибку 400')
    def test_login_without_password_field_returns_400(self):
        with allure.step('Отправляем запрос без поля password'):
            payload = {"login": generate_random_string(10)}
            response = requests.post(f'{BASE_URL}/courier/login', data=payload)

        with allure.step('Проверяем код ответа 400'):
            assert response.status_code == 400

    @allure.title('Логин без обязательного поля возвращает сообщение об ошибке')
    def test_login_missing_field_returns_error_message(self):
        with allure.step('Отправляем запрос без поля login'):
            payload = {"password": generate_random_string(10)}
            response = requests.post(f'{BASE_URL}/courier/login', data=payload)

        with allure.step('Проверяем код ответа 400'):
            assert response.status_code == 400

        with allure.step('Проверяем сообщение об ошибке'):
            assert response.json().get("message") == "Недостаточно данных для входа"

    @allure.title('Логин с неверным паролем возвращает ошибку 404')
    def test_login_with_wrong_password_returns_404(self, new_courier):
        with allure.step('Отправляем запрос с неверным паролем'):
            response = login_courier(new_courier["login"], "wrong_password_xyz")

        with allure.step('Проверяем код ответа 404'):
            assert response.status_code == 404

    @allure.title('Логин с неверным логином возвращает ошибку 404')
    def test_login_with_wrong_login_returns_404(self):
        with allure.step('Отправляем запрос с несуществующим логином'):
            response = login_courier("nonexistent_user_xyz", generate_random_string(10))

        with allure.step('Проверяем код ответа 404'):
            assert response.status_code == 404

    @allure.title('Логин несуществующего пользователя возвращает сообщение об ошибке')
    def test_login_nonexistent_user_returns_error_message(self):
        with allure.step('Отправляем запрос с несуществующим пользователем'):
            response = login_courier("nonexistent_user_xyz", "some_password")

        with allure.step('Проверяем код ответа 404'):
            assert response.status_code == 404

        with allure.step('Проверяем сообщение об ошибке'):
            assert response.json().get("message") == "Учетная запись не найдена"