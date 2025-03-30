from enum import Enum


class TScope(str, Enum):
    @staticmethod
    def get_all_scopes():
        return [x.value for xs in TScope.__subclasses__() for x in xs]
