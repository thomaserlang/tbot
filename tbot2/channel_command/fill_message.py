import re

from tbot2.common import ChatMessageCreate, split

from . import var_fillers as var_fillers
from .types import FillerType, MessageVar, TCommand
from .var_filler import filler_vars, var_filler_registery


async def fill_message(
    *, response_message: str, command: TCommand, chat_message: ChatMessageCreate
) -> str:
    """
    Handle exceptions:
        - CommandError
    """
    parsed_vars = _parse_vars(response_message)

    grouped_func: dict[FillerType, dict[str, MessageVar]] = {}
    for var in parsed_vars:
        if var.name in var_filler_registery:
            grouped_func.setdefault(var_filler_registery[var.name], {})[var.name] = var

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


def _parse_vars(message: str) -> list[MessageVar]:
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


def _fill_response(message: str, values: list[MessageVar]) -> str:
    for var in values:
        if var.value is not None:
            message = message.replace('{' + var.match_raw + '}', str(var.value))
    return message
