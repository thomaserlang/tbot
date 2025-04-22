from urllib.parse import urljoin

from fastapi import Request

from tbot2.config_settings import config


def request_url_for(request: Request, name: str) -> str:
    local_url = request.url_for(name)
    url = urljoin(
        str(config.base_url),
        local_url.path,
    )
    return url
