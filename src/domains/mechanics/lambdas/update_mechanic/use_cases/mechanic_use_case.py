from repositories.mechanic_repository import MechanicRepository


class MechanicUseCase:
    def __init__(self, repository: MechanicRepository):
        self.repository = repository

    def update_mechanic(self, id_mechanic: str, update_data: dict):
        """
        Updates an existing supplier.
        """
        try:
            existing_mechanic = self.repository.find_by_id(id_mechanic)
            if existing_mechanic is None:
                raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')

            result = self.repository.update(id_mechanic, update_data)
            return result
        except Exception as e:
            raise Exception(f'Error al actualizar el mecánico: {str(e)}')
