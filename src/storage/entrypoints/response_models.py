from dataclasses import dataclass


@dataclass
class FileResponse:
    id: int
    name: str
    url: str
