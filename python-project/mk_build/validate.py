from typing import Type, TypeGuard, TypeVar

from .message import invalid_type

_T = TypeVar("_T")


def ensure_type(obj, expected_type: Type[_T]) -> TypeGuard[_T]:
    if not isinstance(obj, expected_type):
        raise TypeError(invalid_type.format(obj, expected_type, type(obj)))

    return True
