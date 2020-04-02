# currency.com API doc: https://exchange.currency.com/api (which is based on binance.com API doc)
# some ideas are taken from https://github.com/toshima/binance/blob/master/binance.py


from tests.utils.http_manager import request, signed_request


# ---------- Requests without authorization:

def ticker():
    """Get best price/qty on the order book for all symbols."""
    data = request("GET", "/ticker/24hr", {'symbol': 'BTC/USD'})
    return data


def all_tickers():
    """Get best price/qty on the order book for all symbols."""
    data = request("GET", "/ticker/24hr")
    return data


# ---------- With authorization:

def balances():
    """Get current balances for all symbols."""
    data = signed_request("GET", "/account")
    return data


def order(symbol, side, quantity, price, order_type, time_in_force='GTC', **kwargs):
    """Send in a new order."""
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "timeInForce": time_in_force,
        "quantity": quantity,
        "price": price,
    }
    params.update(kwargs)
    path = "/order"
    data = signed_request("POST", path, params)
    return data


def cancel_order(symbol, **kwargs):
    """Cancel an active order."""
    params = {"symbol": symbol}
    params.update(kwargs)
    data = signed_request("DELETE", "/order", params)
    return data

