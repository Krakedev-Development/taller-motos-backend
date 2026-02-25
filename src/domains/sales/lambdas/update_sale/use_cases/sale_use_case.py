from repositories.sale_repository import SaleRepository


class SaleUseCase:
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def update_product(self, id_sale: str, update_data: dict):
        """
        Updates an existing sale.
        """
        try:
            existing_sale = self.repository.find_by_id(id_sale)
            if existing_sale is None:
                raise Exception(f'No se encontró la cotización con ID {id_sale}')

            result = self.repository.update(id_sale, update_data)
            return result
        except Exception as e:
            raise Exception(f'Error al actualizar la cotización: {str(e)}')