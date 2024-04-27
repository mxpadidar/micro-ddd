from dataclasses import dataclass

from shared.base import BaseQuery


@dataclass
class GetUserQuery(BaseQuery):
    user_id: int
