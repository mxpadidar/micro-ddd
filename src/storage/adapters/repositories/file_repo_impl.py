from sqlalchemy.orm import Session

from shared.errors import NotFoundError
from storage.domain.entities.file import File
from storage.domain.repositories.file_repo import FileRepo


class FileRepoImpl(FileRepo):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _add(self, file: File) -> None:
        self.session.add(file)

    def _get(self, id: int) -> File:
        file = self.session.query(File).filter_by(id=id).first()
        if not file:
            raise NotFoundError
        return file

    def refresh(self, file: File) -> None:
        self.session.refresh(file)
