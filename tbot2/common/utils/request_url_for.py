from fastapi import Request
from starlette.datastructures import URL

from tbot2.config_settings import config


def request_url_for(request: Request, name: str) -> URL:
    url = request.url_for(name).replace(
        hostname=config.web.base_url.host,
        port=config.web.base_url.port,
        scheme=config.web.base_url.scheme,
    )
    return url
