from shared.auth_service import AuthService
from shared.message_broker import MessageBroker
from storage.domain.s3_client import S3Client
from storage.domain.unit_of_work import UnitOfWork


class Container:
    def __init__(
        self,
        uow: UnitOfWork,
        s3_client: S3Client,
        message_broker: MessageBroker,
        auth_service: AuthService,
    ):
        self._uow = uow
        self._s3_client = s3_client
        self._message_broker = message_broker
        self._auth_service = auth_service

    @property
    def uow(self):
        return self._uow

    @property
    def s3_client(self):
        return self._s3_client

    @property
    def message_broker(self):
        return self._message_broker

    @property
    def auth_service(self):
        return self._auth_service
