from shared.base import BaseModel


class File(BaseModel):
    category: str
    name: str
    mime_type: str
    size: int

    def __init__(self, category: str, name: str, mime_type: str, size: int) -> None:
        self.category = category
        self.name = name
        self.mime_type = mime_type
        self.size = size
        super().__init__()

    @property
    def object_name(self) -> str:
        return f"{self.category}/{self.name}"

    def serialize(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "category": self.category,
            "name": self.name,
            "mime_type": self.mime_type,
            "size": self.size,
            **kwargs,
        }
