import re
import logging
from typing import Optional

from repositories.product_repository import ProductRepository
from repositories.sale_detail_repository import SaleDetailRepository
from repositories.sale_repository import SaleRepository

logger = logging.getLogger(__name__)


class SaleUseCase:
    def __init__(self, sale_repository: SaleRepository,
                 sale_detail_repository: SaleDetailRepository,
                 ):
        self.sale_repository = sale_repository
        self.sale_detail_repository = sale_detail_repository

    def add_sale(self, sale_data: dict) -> dict:
        logger.info("Begin add_sale")
        logger.debug(f"sale_data: {sale_data}")


        try:
            inserted_sale = self.sale_repository.save(sale_data)
            return inserted_sale

        except Exception as e:
            logger.error(f"Error al registrar la venta: {e}")

            raise Exception(f"No se pudo insertar la venta: {e}")

    @staticmethod
    def _extract_invalid_uuid(msg: str) -> Optional[str]:
        """Extrae el UUID inválido de un mensaje de error si existe"""
        match = re.search(r'uuid: "([^"]+)"', msg)
        return match.group(1) if match else None
