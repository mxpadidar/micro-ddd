from shared.base import BaseEntity


class File(BaseEntity):
    bucket: str
    name: str
    mime_type: str
    size: int
    used: bool

    def __init__(self, bucket: str, name: str, mime_type: str, size: int) -> None:
        self.bucket = bucket
        self.name = name
        self.mime_type = mime_type
        self.size = size
        self.used = False
        super().__init__()

    @property
    def object_name(self) -> str:
        return f"{self.bucket}/{self.name}"

    def serialize(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "bucket": self.bucket,
            "name": self.name,
            "mime_type": self.mime_type,
            "size": self.size,
            **kwargs,
        }

    @staticmethod
    def valid_mime_types() -> list[str]:
        return ["image/jpeg", "image/png"]
