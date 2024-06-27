from typing import Type, TypeGuard, TypeVar

from .message import invalid_type

_T = TypeVar("_T")


def check_type(
    obj,
    expected_type: Type[_T],
    message=None
) -> TypeGuard[_T]:
    if not isinstance(obj, expected_type):
        if message is None:
            raise TypeError(invalid_type.format(obj, expected_type, type(obj)))
        else:
            raise TypeError(message)

    return True


def ensure_type(
    obj,
    expected_type: Type[_T],
    message=None
) -> _T:
    if not isinstance(obj, expected_type):
        if message is None:
            raise TypeError(invalid_type.format(obj, expected_type, type(obj)))
        else:
            raise TypeError(message)

    return obj
