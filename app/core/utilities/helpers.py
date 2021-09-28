import threading
from typing import Type, Any, Any


class SingletonMixin(object):
    _instance = None
    _lock = threading.RLock()
    _inner_instance = None

    @classmethod
    def instance(cls: Type[Any], *args: Any, **kwargs: Any) -> Any:
        if cls._instance is not None:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._inner_instance = True
                try:
                    cls._instance = cls(*args, **kwargs)
                finally:
                    cls._inner_instance = False
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls is SingletonMixin:
            raise TypeError(f"Attempt to instantiate mixin class {cls.__qualname__}")

        if cls._instance is None:
            with cls._lock:
                if cls._instance is None and cls._inner_instance:
                    return super().__new__(cls, *args, **kwargs)

        raise RuntimeError(
            f"Attempt to create a {cls.__qualname__} instance outside of instance()"
        )
