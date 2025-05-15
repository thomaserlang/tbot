from pydantic import BaseModel, ConfigDict


class BaseRequestSchema(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        from_attributes=True,
        validate_by_name=True,
        validate_by_alias=True,
        validate_assignment=True,
    )
