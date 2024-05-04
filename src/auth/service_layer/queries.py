from dataclasses import dataclass

from shared.base import Query


@dataclass
class GetUserQuery(Query):
    user_id: int
