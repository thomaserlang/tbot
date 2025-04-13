from enum import StrEnum


class Scope(StrEnum):
    @staticmethod
    def get_all_scopes() -> list[str]:
        return [x.value for xs in Scope.__subclasses__() for x in xs]
