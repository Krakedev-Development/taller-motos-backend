import logging
import re
from core.repository import BulkProductRepository

logger = logging.getLogger(__name__)


class BulkProductUseCase:
    def __init__(self, repository: BulkProductRepository):
        self.repository = repository

    def execute_bulk_insert(self, products_data: dict):
        """
        Executes the bulk insert of products.
        """
        logger.info("Starting BulkProductUseCase execution")
        try:
            inserted_products = self.repository.bulk_save(products_data)
            return inserted_products
        except Exception as e:
            msg = str(e)
            logger.error(f"Error in BulkProductUseCase.execute_bulk_insert: {msg}")

            # Extract UUID from error if possible
            uuid_invalid = None
            match = re.search(r'uuid: "([^"]+)"', msg)
            if match:
                uuid_invalid = match.group(1)

            if uuid_invalid:
                raise Exception(f"No se pudo insertar la carga masiva: el id '{uuid_invalid}' no es un UUID válido")
            else:
                raise Exception(f"No se pudo realizar la carga masiva: {msg}")
