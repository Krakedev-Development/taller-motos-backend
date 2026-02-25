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
                 product_repository: ProductRepository):
        self.sale_repository = sale_repository
        self.sale_detail_repository = sale_detail_repository
        self.product_repository = product_repository

    def add_sale(self, sale_data: dict) -> dict:
        logger.info("Begin add_sale")
        logger.debug(f"sale_data: {sale_data}")

        sale = sale_data["sale"]
        details = sale_data["details"]
        products = sale_data["products"]
        inserted_sale = None

        try:
            inserted_sale = self.sale_repository.save(sale)

            inserted_details = []
            for detail_item in details:
                inserted_detail = self.sale_detail_repository.save(detail_item)
                if inserted_detail:
                    stock_product = products[detail_item["id_product"]]["new_stock"]
                    self.product_repository.update_stock(detail_item["id_product"], stock_product)
                    inserted_details.append(inserted_detail)

            return {
                "sale": inserted_sale,
                "details": inserted_details
            }

        except Exception as e:
            logger.error(f"Error al registrar la venta: {e}")

            if inserted_sale:
                self.sale_detail_repository.delete(inserted_sale["id_sale"])
                self.sale_repository.delete(inserted_sale["id_sale"])
                for detail_item in details:
                    stock_product = products[detail_item["id_product"]]["current_stock"]
                    self.product_repository.update_stock(detail_item["id_product"], stock_product)

            uuid_invalid = self._extract_invalid_uuid(str(e))
            if uuid_invalid:
                raise Exception(f"No se pudo insertar la venta: el id '{uuid_invalid}' no es un UUID válido")
            raise Exception(f"No se pudo insertar la venta: {e}")

    @staticmethod
    def _extract_invalid_uuid(msg: str) -> Optional[str]:
        """Extrae el UUID inválido de un mensaje de error si existe"""
        match = re.search(r'uuid: "([^"]+)"', msg)
        return match.group(1) if match else None
