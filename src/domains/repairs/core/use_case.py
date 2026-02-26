import math
import re
import logging
from core.repository import RepairRepository

logger = logging.getLogger(__name__)

class RepairUseCase:
    def __init__(self, repository: RepairRepository):
        self.repository = repository

    def get_repairs(self, page: int = 1, limit: int = 10, search: str = None):
        data, total = self.repository.find_all(page, limit, search)
        total_pages = math.ceil(total / limit) if limit > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": total_pages
            },
        }

    def get_repair_by_id(self, id_repair: str):
        result = self.repository.find_by_id(id_repair)
        if result is None:
            raise Exception(f'No se encontró la reparación con ID {id_repair}')
        return result

    def add_repair(self, repair_data: dict):
        try:
            # Handle photos if present in repair_data
            if "photos" in repair_data and repair_data["photos"]:
                urls = self.repository.upload_photos("repairs", repair_data["photos"])
                repair_data["repair"]["photos"] = urls

            result = self.repository.save_transaction(repair_data)
            return result
        except Exception as e:
            logger.error(f"Error al registrar la reparacion: {e}")
            msg = str(e)
            match = re.search(r'uuid: "([^"]+)"', msg)
            if match:
                uuid_invalid = match.group(1)
                raise Exception(f"No se pudo insertar la reparacion: el id '{uuid_invalid}' no es un UUID válido")
            raise Exception(f"No se pudo insertar la reparacion: {msg}")

    def delete_repair(self, id_repair: str):
        # Check existence
        existing = self.repository.find_by_id(id_repair)
        if existing is None:
            raise Exception(f'No se encontró la reparación con ID {id_repair}')
        
        # In a real scenario, we might want to delete materials and services if the DB doesn't handle CASCADE
        # Let's keep the logic from delete_repair lambda
        try:
            self.repository.delete_materials(id_repair)
            self.repository.delete_services(id_repair)
            return self.repository.delete(id_repair)
        except Exception as e:
            raise Exception(f"Error al eliminar la reparación: {str(e)}")

    def update_repair(self, id_repair: str, update_data: dict):
        existing = self.repository.find_by_id(id_repair)
        if existing is None:
            raise Exception(f'No se encontró la reparación con ID {id_repair}')
        
        try:
            return self.repository.update(id_repair, update_data)
        except Exception as e:
            raise Exception(f"Error al actualizar la reparación: {str(e)}")

    def save_images(self, photos: list) -> list:
        try:
            return self.repository.upload_photos("repairs", photos)
        except Exception as e:
            raise Exception(f"Error al registrar las imagenes: {e}")
