from auth.domain.jwt_service import JWTService
from auth.domain.unit_of_work import UnitOfWork
from auth.domain.user_manager import UserManager
from shared.message_broker import MessageBroker
from shared.storage_service import StorageService


class Container:
    def __init__(
        self,
        uow: UnitOfWork,
        storage_service: StorageService,
        message_broker: MessageBroker,
        user_manager: UserManager,
        jwt_service: JWTService,
    ):
        self._uow = uow
        self._storage_service = storage_service
        self._message_broker = message_broker
        self._user_manager = user_manager
        self._jwt_service = jwt_service

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
    def user_manager(self):
        return self._user_manager

    @property
    def jwt_service(self):
        return self._jwt_service
