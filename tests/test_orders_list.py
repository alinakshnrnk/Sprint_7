import requests
import allure
from helpers.courier_helpers import (
    BASE_URL,
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier,
)


@allure.feature('Список заказов')
class TestGetOrdersList:

    @allure.title('Без параметров возвращается список заказов')
    def test_get_orders_returns_list(self):
        with allure.step('Отправляем GET /orders без параметров'):
            response = requests.get(f'{BASE_URL}/orders')

        with allure.step('Проверяем код ответа 200'):
            assert response.status_code == 200

        with allure.step('Проверяем наличие списка orders в теле ответа'):
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)

    @allure.title('С параметрами limit и page возвращается список заказов')
    def test_get_orders_with_limit_and_page(self):
        with allure.step('Отправляем GET /orders с limit=10 и page=0'):
            response = requests.get(f'{BASE_URL}/orders', params={"limit": 10, "page": 0})

        with allure.step('Проверяем код ответа 200'):
            assert response.status_code == 200

        with allure.step('Проверяем список и соблюдение лимита'):
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)
            assert len(response.json()["orders"]) <= 10

    @allure.title('С фильтром nearestStation возвращается список заказов')
    def test_get_orders_with_nearest_station_filter(self):
        with allure.step('Отправляем GET /orders с nearestStation=["110"]'):
            response = requests.get(
                f'{BASE_URL}/orders',
                params={"limit": 10, "page": 0, "nearestStation": '["110"]'},
            )

        with allure.step('Проверяем код ответа 200'):
            assert response.status_code == 200

        with allure.step('Проверяем наличие списка orders в теле ответа'):
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)

    @allure.title('С параметром courierId возвращаются заказы курьера')
    def test_get_orders_by_courier_id(self):
        with allure.step('Регистрируем и логиним курьера'):
            creds = register_new_courier_and_return_login_password()
            assert creds, "Не удалось зарегистрировать курьера"
            login, password, _ = creds
            login_response = login_courier(login, password)
            assert login_response.status_code == 200
            courier_id = login_response.json()["id"]

        with allure.step(f'Отправляем GET /orders?courierId={courier_id}'):
            response = requests.get(f'{BASE_URL}/orders', params={"courierId": courier_id})

        with allure.step('Проверяем код ответа 200'):
            assert response.status_code == 200

        with allure.step('Проверяем наличие списка orders в теле ответа'):
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)

        with allure.step('Удаляем курьера'):
            delete_courier(courier_id)

    @allure.title('С courierId и nearestStation возвращаются заказы курьера на станциях')
    def test_get_orders_by_courier_id_with_station_filter(self):
        with allure.step('Регистрируем и логиним курьера'):
            creds = register_new_courier_and_return_login_password()
            assert creds, "Не удалось зарегистрировать курьера"
            login, password, _ = creds
            login_response = login_courier(login, password)
            assert login_response.status_code == 200
            courier_id = login_response.json()["id"]

        with allure.step('Отправляем GET /orders с courierId и nearestStation'):
            response = requests.get(
                f'{BASE_URL}/orders',
                params={"courierId": courier_id, "nearestStation": '["1", "2"]'},
            )

        with allure.step('Проверяем код ответа 200'):
            assert response.status_code == 200

        with allure.step('Проверяем наличие списка orders в теле ответа'):
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)

        with allure.step('Удаляем курьера'):
            delete_courier(courier_id)

    @allure.title('С несуществующим courierId возвращается ошибка 404')
    def test_get_orders_with_nonexistent_courier_id_returns_404(self):
        with allure.step('Отправляем GET /orders с несуществующим courierId'):
            response = requests.get(f'{BASE_URL}/orders', params={"courierId": 999999999})

        with allure.step('Проверяем код ответа 404'):
            assert response.status_code == 404

        with allure.step('Проверяем наличие message в теле ответа'):
            assert "message" in response.json()