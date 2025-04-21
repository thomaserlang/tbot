from tbot2.exceptions import ErrorMessage


class CommandError(ErrorMessage): ...


class CommandSyntaxError(CommandError): ...
