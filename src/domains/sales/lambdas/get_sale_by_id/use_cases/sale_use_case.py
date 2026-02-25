from repositories.sale_repository import SaleRepository


class SaleUseCase:
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def find_sale_by_id(self, id_sale: str):
        """
        Busca una venta por ID.
        """
        try:
            result = self.repository.find_by_id(id_sale)
            if result is None:
                raise Exception(f'No se encontró la venta con ID {id_sale}')


            return result

        except Exception as e:
            raise Exception(f'Error al buscar la venta: {str(e)}')
