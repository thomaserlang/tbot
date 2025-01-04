import re
from typing import Literal, Sequence

from tbot2.common import ChatMessage, TProvider, split

from .types import Command, FillVars, MessageVar, TFillerType

__all__ = [
    'fills_vars',
    'fill_message',
    'fill_from_dict',
]


var_fillers: dict[str, TFillerType] = {}
filler_vars: dict[TFillerType, FillVars] = {}


def fills_vars(provider: Literal['all'] | TProvider, vars: Sequence[str]):
    def decorator(func: TFillerType):
        for var in vars:
            var_fillers[var] = func
        filler_vars[func] = FillVars(provider=provider, vars=vars)
        return func

    return decorator


async def fill_message(
    *, response_message: str, command: Command, chat_message: ChatMessage
):
    parsed_vars = _parse_vars(response_message)

    grouped_func: dict[TFillerType, dict[str, MessageVar]] = {}
    for var in parsed_vars:
        if var.name in var_fillers:
            grouped_func.setdefault(var_fillers[var.name], {})[var.name] = var

    for func in grouped_func:
        vars: dict[str, MessageVar] = {}
        if (
            filler_vars[func].provider != chat_message.provider
            and filler_vars[func].provider != 'all'
        ):
            continue
        for var_name in filler_vars[func].vars:
            if var_name not in grouped_func[func]:
                vars[var_name] = MessageVar(name=var_name, match_raw=var_name, args=[])
            else:
                vars[var_name] = grouped_func[func][var_name]
        await func(chat_message, command, vars)
    return _fill_response(response_message, parsed_vars)


def _parse_vars(message: str):
    matched: list[str] = re.findall(
        r'\{([a-z0-9]+[ ]?.*?)\}', message, flags=re.IGNORECASE
    )
    vars: list[MessageVar] = []
    for match in matched:
        name, *args = split(match)
        vars.append(
            MessageVar(
                match_raw=match,
                found=True,
                name=name,
                args=args,
            )
        )
    return vars


def _fill_response(message: str, values: list[MessageVar]):
    for var in values:
        if var.value is not None:
            message = message.replace('{' + var.match_raw + '}', str(var.value))
    return message


def fill_from_dict(message: str, data: dict[str, str | int]):
    for k in data:
        message = message.replace('{' + k + '}', str(data[k]))
    return message
