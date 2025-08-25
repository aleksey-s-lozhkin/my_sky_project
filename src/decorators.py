from typing import Callable, ParamSpec, TypeVar
from datetime import datetime
from functools import wraps


P = ParamSpec('P')
T = TypeVar('T')


def log(filename: str = "mylog.txt") -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Декоратор, который автоматически логирует начало и конец выполнения функции, а также ее результаты или возникшие
    ошибки. Декоратор принимает необязательный аргумент filename, который определяет, куда будут записываться логи (в
    файл или в консоль). Если filename задан, логи записываются в указанный файл. Если filename не задан, логи выводятся
    в консоль."""

    def wrapper(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> T:
            log_msg = ''
            start_func = datetime.now()
            start_msg = f'{start_func} start "{func.__name__}"\n'
            log_msg += start_msg

            try:
                result = func(*args, **kwargs)
                end_func = datetime.now()
                end_msg = f'{end_func} stop "{func.__name__}"\n'
                log_msg += end_msg
                func_result = f'"{func.__name__}" ok\n'
                log_msg += func_result

            except Exception as err:
                end_func = datetime.now()
                end_msg = f'{end_func} stop "{func.__name__}"\n'
                log_msg += end_msg
                func_result = f'"{func.__name__}" error: {err}. Inputs: {args}, {kwargs}\n'
                log_msg += func_result

            finally:
                if filename:
                    with open(filename, 'a') as log_file:
                        log_file.write(log_msg)
                else:
                    print(log_msg)

            return result

        return inner

    return wrapper
