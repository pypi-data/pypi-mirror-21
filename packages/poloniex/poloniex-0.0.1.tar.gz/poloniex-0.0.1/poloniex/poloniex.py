import hmac as _hmac
import time as _time
import hashlib as _hashlib
import requests as _requests
import functools as _functools
import itertools as _itertools
import threading as _threading

from .utils import AutoCastDict
from .exceptions import *


_PUBLIC_URL = 'https://poloniex.com/public'
_PRIVATE_URL = 'https://poloniex.com/private'


class PoloniexPublic(object):

    """Client to connect to Poloniex public APIs"""

    def __init__(self, public_url=_PUBLIC_URL, limit=6):
        """Initialize Poloniex client."""
        self._public_url = public_url
        self._public_session = _requests.Session()
        self._semaphore = _threading.Semaphore(limit)

    @staticmethod
    def _sanitize_parameters(params):
        """Sanitize the params removing none values."""
        return {key: val for key, val in params.items() if val is not None}

    def _public(self, command, **params):
        """Invoke the 'command' public API with optional params."""
        params = self._sanitize_parameters(params)
        params['command'] = command
        response = self._public_session.get(self._public_url, params=params)
        return response.json(object_hook=AutoCastDict)

    def returnTicker(self):
        """Returns the ticker for all markets."""
        return self._public('returnTicker')

    def return24hVolume(self):
        """Returns the 24-hour volume for all markets, plus totals for
        primary currencies."""
        return self._public('return24hVolume')

    def returnOrderBook(self, currencyPair='all', depth='50'):
        """Returns the order book for a given market, as well as a sequence
        number for use with the Push API and an indicator specifying whether
        the market is frozen. You may set currencyPair to "all" to get the
        order books of all markets."""
        return self._public('returnOrderBook', currencyPair=currencyPair,
                            depth=depth)

    def returnTradeHistory(self, currencyPair, start=None, end=None):
        """Returns the past 200 trades for a given market, or up to 50,000
        trades between a range specified in UNIX timestamps by the "start"
        and "end" GET parameters."""
        return self._public('returnTradeHistory', currencyPair=currencyPair,
                            start=start, end=end)

    def returnChartData(self, currencyPair, period, start, end):
        """Returns candlestick chart data. Required GET parameters are
        "currencyPair", "period" (candlestick period in seconds; valid values
        are 300, 900, 1800, 7200, 14400, and 86400), "start", and "end".
        "Start" and "end" are given in UNIX timestamp format and used to
        specify the date range for the data returned."""
        return self._public('returnChartData', currencyPair=currencyPair,
                            period=period, start=start, end=end)

    def returnCurrencies(self):
        """Returns information about currencies."""
        return self._public('returnCurrencies')

    def returnLoanOrders(self, currency):
        """Returns the list of loan offers and demands for a given currency,
        specified by the "currency" GET parameter."""
        return self._public('returnLoanOrders', currency=currency)


class Poloniex(PoloniexPublic):

    """Client to connect to Poloniex private APIs."""

    class _PoloniexAuth(_requests.auth.AuthBase):

        """Poloniex Request Authentication."""

        def __init__(self, secret):
            self._secret = secret

        def __call__(self, request):
            signature = _hmac.new(self._secret, request.body, _hashlib.sha512)
            request.headers['Sign'] = signature.hexdigest()
            print request.headers
            return request


    def __init__(self, apikey=None, secret=None, public_url=_PUBLIC_URL,
                 private_url=_PRIVATE_URL, limit=6):
        """Initialize the Poloniex private client."""
        PoloniexPublic.__init__(self, public_url, limit)
        self._private_url = private_url
        self._private_session = _requests.Session()
        self._private_session.headers['Key'] = self._apikey = apikey
        self._secret = secret
        self._nonces = _itertools.count(int(_time.time() * 1000))

    def _private(self, method, command, **params):
        """Invoke the 'command' public API with optional params."""
        if not self._apikey or not self._secret:
            raise PoloniexCredentialsException('missing apikey/secret')

        params = self._sanitize_parameters(params)
        params.update({'command': command, 'nonce': next(self._nonces)})
        response = self._private_session.request(method, self._private_url,
                params=params, auth=Poloniex._PoloniexAuth(self._secret))
        print response.status_code
        print response.content
        return response.json(object_hook=AutoCastDict)
