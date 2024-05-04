from typing import Callable, Type

from auth.domain.unit_of_work import UnitOfWork
from auth.service_layer.queries import GetUserQuery
from shared.base import Query
from shared.storage_service import StorageService


def get_user_query_handler(
    query: GetUserQuery, uow: UnitOfWork, storage_service: StorageService
):
    with uow:
        user = uow.users.get(id=query.user_id)
        avatar = (
            storage_service.get_file_by_id(user.avatar_file_id)
            if user.avatar_file_id
            else None
        )
        return user.serialize(avatar=avatar)


query_handlers_mapper: dict[Type[Query], Callable] = {
    GetUserQuery: get_user_query_handler,
}