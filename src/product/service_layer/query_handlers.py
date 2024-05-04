from typing import Callable, Type

from shared.base import Query

query_handlers_mapper: dict[Type[Query], Callable] = {}
