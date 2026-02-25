from repositories.mechanic_repository import MechanicRepository


class MechanicUseCase:
    def __init__(self, repository: MechanicRepository):
        self.repository = repository

    def delete_mechanic(self, id_mechanic: str):
        """
        Elimina un mecánico de la base de datos.
        """
        try:
            existing_customer = self.repository.find_by_id(id_mechanic)
            if existing_customer is None:
                raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')

            result = self.repository.delete(id_mechanic)
            return result
        except Exception as e:
            raise Exception(f'Error al eliminar el mecánico: {str(e)}')
