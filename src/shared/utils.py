import inspect
from typing import Callable


def inject_dependencies(handler: Callable, dependencies: dict):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
