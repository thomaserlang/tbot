from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


def _deep_update(source: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively merge two dictionaries: overrides into source.
    Values in overrides will overwrite or merge into source.
    """
    for key, value in overrides.items():
        if key in source and isinstance(source[key], dict) and isinstance(value, dict):
            source[key] = _deep_update(source[key], value)  # type: ignore
        else:
            source[key] = value
    return source


def update_model(
    original: T, updates: BaseModel, model_cls: type[T] | None = None
) -> T:
    """
    Returns a new Pydantic v2 model instance by merging `updates`
    (only set fields) into `original`, without overwriting nested objects.
    """
    model_cls = model_cls or type(original)
    orig_data = original.model_dump()
    update_data = updates.model_dump(exclude_unset=True)

    merged = _deep_update(orig_data, update_data)

    return model_cls.model_validate(merged)
