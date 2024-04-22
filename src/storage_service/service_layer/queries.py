from dataclasses import dataclass

from shared.base import BaseQuery


@dataclass
class GetFileQuery(BaseQuery):
    file_id: int
