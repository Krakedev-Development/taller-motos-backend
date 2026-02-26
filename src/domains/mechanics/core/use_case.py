import math
from core.repository import MechanicRepository

class MechanicUseCase:
    def __init__(self, repository: MechanicRepository):
        self.repository = repository

    def get_mechanics(self, page: int = 1, limit: int = 10, search: str = None):
        data, total = self.repository.find_all(page, limit, search)
        total_pages = math.ceil(total / limit) if limit > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": total_pages
            }
        }

    def get_mechanic_by_id(self, id_mechanic: str):
        result = self.repository.find_by_id(id_mechanic)
        if result is None:
            raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')
        return result

    def add_mechanic(self, mechanic_data: dict):
        return self.repository.save(mechanic_data)

    def update_mechanic(self, id_mechanic: str, update_data: dict):
        existing = self.repository.find_by_id(id_mechanic)
        if existing is None:
            raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')
        return self.repository.update(id_mechanic, update_data)

    def delete_mechanic(self, id_mechanic: str):
        existing = self.repository.find_by_id(id_mechanic)
        if existing is None:
            raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')
        return self.repository.delete(id_mechanic)
