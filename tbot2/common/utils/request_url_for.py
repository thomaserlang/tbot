from fastapi import Request
from starlette.datastructures import URL

from tbot2.config_settings import config


def request_url_for(request: Request, name: str) -> URL:
    url = request.url_for(name).replace(
        hostname=config.base_url.host,
        port=config.base_url.port,
        scheme=config.base_url.scheme,
    )
    return url
