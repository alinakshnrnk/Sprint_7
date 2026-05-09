import requests
import allure
import pytest
from helpers.courier_helpers import BASE_URL


ORDER_BASE_PAYLOAD = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha",
}


@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа с цветом самоката: {color}')
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],
    ])
    def test_create_order_with_color_options(self, color):
        with allure.step(f'Отправляем POST /orders с color={color}'):
            payload = {**ORDER_BASE_PAYLOAD, "color": color}
            response = requests.post(f'{BASE_URL}/orders', json=payload)

        with allure.step('Проверяем код ответа 201'):
            assert response.status_code == 201

        with allure.step('Проверяем наличие track в теле ответа'):
            assert "track" in response.json()
            assert response.json()["track"] is not None