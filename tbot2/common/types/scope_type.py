from enum import StrEnum


class TScope(StrEnum):
    @staticmethod
    def get_all_scopes():
        return [x.value for xs in TScope.__subclasses__() for x in xs]
