from shared.db_setup import registry
from storage_service.adapters.orm.tables import files
from storage_service.domain.models.file import File


def start_mappers():

    registry.map_imperatively(File, files)
