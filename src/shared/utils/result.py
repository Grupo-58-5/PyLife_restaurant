from typing import TypeVar

T = TypeVar("T")

class Result[T]:

    value:T
    error: BaseException
    messg: str
    is_failure: bool

    def __init__(self, value: T | None, error: BaseException | None = None, messg: str | None = None, code: int | None = None) :
        if (value is None) and (error is None):
            raise ValueError("The result must recibe one input, this has both attributes as None")
        if (value is not None) and (error is not None):
            raise ValueError("The result must recibe JUST ONE input, this has both attributes value, and error with values ")

        self.error = error
        self.value = value
        self.messg = messg
        self.code = code

    def get_error_message(self) -> str:
        if (self.error is None):
            raise 'There is no Error message, this may be OK'
        return self.messg

    def get_error_code(self) -> int:
        if (self.error is None):
            raise 'There is no Error code, this may be OK'
        return self.code

    def result(self) -> T:
        if(self.value is None):
            raise ValueError("There is no value, this may be an error")
        return self.value

    def is_succes(self) -> bool:
        return self.value is not None

    def is_error(self) -> bool :
        return self.error is not None

    @staticmethod
    def success(value: T):
        return Result(value=value, error=None)

    @staticmethod
    def failure(error: BaseException, messg: str, code: int | None = None):
        return Result(value=None, error=error,messg=messg,code=code)