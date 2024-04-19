from auth_service.adapters.orm.tables import users
from auth_service.domain.models.user import User
from shared.db_setup import registry


def start_mappers():
    registry.map_imperatively(User, users)
