from pydantic import BaseModel, ConfigDict


class BaseRequestSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')
