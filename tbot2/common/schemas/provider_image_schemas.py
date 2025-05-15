from .base_schema import BaseSchema
from .image_urls_schema import ImageUrls


class ProviderImage(BaseSchema):
    name: str
    animated: bool = False
    urls: ImageUrls
