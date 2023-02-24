
from typing import Any
from .option import Option, some


"""
"""
class Error(object):
    def __init__(self, msg: str, exp: Exception) -> None:
        self._message = msg
        self._exception = exp

    def __str__(self) -> str:
        return f"{self._message}"

    @staticmethod
    def from_msg(msg: str) -> object:
        return Error(msg, None)


"""
"""
class Result(object):
    def __init__(self, res: Any, err: Error) -> None:
        self._err = err
        self._result = Option(res)

    def __del__(self) -> None:
        self._err = None
        self._result = None

    def __str__(self) -> str:
        return str(self._err) if self.is_error() else ""

    """
    """
    def is_error(self) -> bool:
        return isinstance(self._err, Error)

    """
    """
    def is_ok(self) -> bool:
        return not isinstance(self._err, Error)

    """
    """
    def result(self) -> Option:
        return self._result

    """
    """
    def err(self) -> Error:
        return self._err


def error(exp: Error) -> Result:
    return Result(None, exp)


def result(res: Any) -> Result:
    return Result(res, None)


def ok() -> Result:
    return Result(None, None)


"""
err = error(Error.from_msg("Some error"))
non = ok()

print(err)
print(non)
"""
