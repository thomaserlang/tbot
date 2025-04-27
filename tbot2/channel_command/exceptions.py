from tbot2.common.exceptions import ErrorMessage


class CommandError(ErrorMessage): ...


class CommandSyntaxError(CommandError): ...
