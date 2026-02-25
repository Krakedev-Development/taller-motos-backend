from entities.product import Product
from repositories.product_repository import ProductRepository


class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    def delete_product(self, id_product: str):
        """
        Deletes a product from the database.
        """
        try:
            existing_product = self.repository.find_by_id(id_product)
            if existing_product is None:
                raise Exception(f'No se encontró el producto con ID {id_product}')
            
            result = self.repository.delete(id_product)
            return result
        except Exception as e:
            raise Exception(f'Error al eliminar el producto: {str(e)}')