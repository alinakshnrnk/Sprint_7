import requests
import allure
import pytest
from payloads import ORDER_BASE_PAYLOAD
from urls import ORDERS_URL


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
            response = requests.post(ORDERS_URL, json=payload)

        with allure.step('Проверяем код ответа 201'):
            assert response.status_code == 201

        with allure.step('Проверяем наличие track в теле ответа'):
            assert "track" in response.json()
            assert response.json()["track"] is not None