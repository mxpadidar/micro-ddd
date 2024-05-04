from shared.db_setup import registry
from storage.adapters.orm.tables import files
from storage.domain.entities.file import File


def start_mappers():

    registry.map_imperatively(File, files)
