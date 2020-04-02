import time
import pytest
from tests.utils.api import *
# import logging


# log = logging.getLogger()


@pytest.mark.unauthorized
def test_all_tickers():
    """Get all tickers"""
    result = all_tickers()
    response_body = result.json()  # it's a list containing dictionaries (objects)

    # Response code is 200
    assert 200 == result.status_code

    # Number of markets is > 1000
    assert 1000 < len(response_body)

    # Total trade volume for 24hrs is > 50 000 USD
    total_volume = 0
    for i in response_body:
        total_volume += float(i['volume'])
    assert 50000 < total_volume

    # Response data is valid
    for i in response_body:
        assert i['symbol']
        # assert i['weightedAvgPrice'] != 0  # sometimes fails due to wrong instruments data
        # assert i['lastPrice'] != 0  # sometimes fails due to wrong instruments data
        # assert i['lastQty'] != 0  # sometimes fails due to wrong instruments data
        # assert i['bidPrice'] != 0  # sometimes fails due to wrong instruments data
        # assert i['askPrice'] != 0  # sometimes fails due to wrong instruments data
        # assert i['highPrice'] != 0  # sometimes fails due to wrong instruments data
        # assert i['lowPrice'] != 0  # sometimes fails due to wrong instruments data
        assert i['volume']
        assert i['quoteVolume']
        assert i['openTime'] != 0
        assert i['closeTime'] != 0

        """
        Example of an object in response:
        {
            "symbol": "BTC/USD",
            "weightedAvgPrice": "6644.45",
            "lastPrice": "6643.80",
            "lastQty": "0.25",
            "bidPrice": "6643.80",
            "askPrice": "6645.10",
            "highPrice": "6912.05",
            "lowPrice": "6065.3",
            "volume": "1129.833",
            "quoteVolume": "7400123.69175",
            "openTime": 1584624694000,
            "closeTime": 1584711094000,
            "firstId": 0,
            "lastId": 0,
            "count": 0
        }
        
        Note: server returns strings where int would do better so we don't validate if type == string
        """

    # All important markets are present in response
    important_markets = ["BTC/USD", "BTC/EUR", "BTC/RUB", "BTC/BYN", "ETH/USD", "ETH/EUR", "ETH/RUB", "ETH/BYN", "ETH/BTC", "LTC/USD", "LTC/EUR"]
    important_markets_count = len(important_markets)
    found_markets = 0
    for i in response_body:
        if i['symbol'] in important_markets:
            found_markets += 1
    assert found_markets == important_markets_count


@pytest.mark.authorized
def test_create_limit_order_wait_and_cancel():
    """Create limit order (BTC/USD), wait, delete order"""

    # Create order
    result = order(symbol='BTC/USD', side='BUY', quantity=0.01, price=4000.01, order_type='LIMIT')
    response_body = result.json()
    # log.info("Create order - Response:")
    # log.info(response_body)
    order_id = response_body['orderId']

    assert 200 == result.status_code

    # Response data is valid
    assert response_body['orderId']
    assert response_body['price']
    assert response_body['side']
    assert response_body['symbol']
    assert response_body['type']

    time.sleep(1)

    # Cancel order
    result = cancel_order(symbol='BTC/USD', orderId=order_id)
    response_body = result.json()
    # log.info("Delete order - Response:")
    # log.info(response_body)

    assert 200 == result.status_code

    # Response data is valid
    assert response_body['orderId'] == order_id
    assert response_body['price']
    assert response_body['side']
    assert response_body['symbol']
    assert response_body['type']
    assert response_body['status'] == 'CANCELED'
