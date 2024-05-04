from auth.adapters.orm.tables import users
from auth.domain.entities.user import User
from shared.db_setup import registry


def start_mappers():
    registry.map_imperatively(User, users)
