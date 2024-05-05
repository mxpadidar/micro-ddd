from product.domain.unit_of_work import UnitOfWork
from shared.auth_service import AuthService
from shared.message_broker import MessageBroker
from shared.storage_service import StorageService


class Container:
    def __init__(
        self,
        uow: UnitOfWork,
        storage_service: StorageService,
        message_broker: MessageBroker,
        auth_service: AuthService,
    ):
        self._uow = uow
        self._storage_service = storage_service
        self._message_broker = message_broker
        self._auth_service = auth_service

    @property
    def uow(self):
        return self._uow

    @property
    def storage_service(self):
        return self.storage_service

    @property
    def message_broker(self):
        return self._message_broker

    @property
    def auth_service(self):
        return self._auth_service
