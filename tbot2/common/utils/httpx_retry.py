from http import HTTPMethod, HTTPStatus

import httpx
from httpx import AsyncHTTPTransport
from httpx_retries import Retry, RetryTransport

retry_transport = RetryTransport(
    retry=Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=frozenset(
            [
                HTTPStatus.TOO_MANY_REQUESTS,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
            ]
        ),
        allowed_methods=frozenset(
            [
                HTTPMethod.HEAD,
                HTTPMethod.GET,
                HTTPMethod.PUT,
                HTTPMethod.POST,
                HTTPMethod.DELETE,
                HTTPMethod.OPTIONS,
                HTTPMethod.TRACE,
            ]
        ),
        retry_on_exceptions=frozenset(
            [
                httpx.TimeoutException,
                httpx.NetworkError,
                httpx.RemoteProtocolError,
                httpx.LocalProtocolError,
            ]
        ),
    ),
    transport=AsyncHTTPTransport(
        http1=True,
        http2=True,
        retries=5,
    ),
)
