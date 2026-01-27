from functools import wraps

from fastapi import HTTPException


def handle_errors(error_map: list[tuple[type[Exception], int, str]]):
    """
    error_map: [(ExceptionClass, http_status, message_template)]
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                for exc_class, status_code, msg_template in error_map:
                    if isinstance(e, exc_class):
                        message = msg_template.format(e=e)
                        raise HTTPException(
                            status_code=status_code,
                            detail=message,
                        ) from e

                raise HTTPException(
                    status_code=500,
                    detail=str(e),
                ) from e

        return wrapper

    return decorator
