from collections.abc import Sequence
from typing import Literal

from tbot2.common import TProvider

from .types import TFillerType, TFillVars

var_filler_registery: dict[str, TFillerType] = {}
filler_vars: dict[TFillerType, TFillVars] = {}


def fills_vars(provider: Literal['all'] | TProvider, vars: Sequence[str]):
    def decorator(func: TFillerType):
        for var in vars:
            var_filler_registery[var] = func
        filler_vars[func] = TFillVars(provider=provider, vars=vars)
        return func

    return decorator
