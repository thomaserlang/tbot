from collections.abc import Callable, Sequence
from typing import Literal

from tbot2.common import Provider

from .types import FillerType, FillVars

var_filler_registery: dict[str, FillerType] = {}
filler_vars: dict[FillerType, FillVars] = {}


def fills_vars(
    provider: Literal['all'] | Provider, vars: Sequence[str]
) -> Callable[[FillerType], FillerType]:
    def decorator(func: FillerType) -> FillerType:
        for var in vars:
            var_filler_registery[var] = func
        filler_vars[func] = FillVars(provider=provider, vars=vars)
        return func

    return decorator
