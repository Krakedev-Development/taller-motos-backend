import math
import logging
import re
from typing import Optional, List, Dict, Any
from core.repository import SaleRepository
from entities.payment_method import PaymentMethod

logger = logging.getLogger(__name__)

class SaleUseCase:
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def get_sales(self, page: int = 1, limit: int = 10, search: str = None, 
                 record_type: str = None, payment_method: str = None):
        try:
            pm = payment_method
            if isinstance(pm, str) and pm.strip().lower() in ("", "null"):
                pm = None
                
            data, total = self.repository.find_all(page, limit, search, record_type, pm)
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
        except Exception as e:
            logger.error(f'Error in SaleUseCase.get_sales: {str(e)}')
            raise

    def get_sale_by_id(self, id_sale: str):
        result = self.repository.find_by_id(id_sale)
        if result is None:
            raise Exception(f'No se encontró la venta con ID {id_sale}')
        return result

    def add_sale(self, sale_data: dict):
        try:
            result = self.repository.save_transaction(sale_data)
            return result
        except Exception as e:
            logger.error(f"Error al registrar la venta: {e}")
            msg = str(e)
            match = re.search(r'uuid: "([^"]+)"', msg)
            if match:
                uuid_invalid = match.group(1)
                raise Exception(f"No se pudo insertar la venta: el id '{uuid_invalid}' no es un UUID válido")
            raise Exception(f"No se pudo insertar la venta: {msg}")

    def update_sale(self, id_sale: str, update_data: dict):
        """Updates an existing sale (usually a quote)"""
        try:
            existing_sale = self.repository.find_by_id_raw(id_sale)
            if existing_sale is None:
                raise Exception(f'No se encontró la venta/cotización con ID {id_sale}')

            result = self.repository.update(id_sale, update_data)
            return result
        except Exception as e:
            logger.error(f"Error updating sale: {e}")
            raise Exception(f'Error al actualizar la venta: {str(e)}')

    def delete_sale(self, id_sale: str):
        try:
            # Check existence
            existing = self.repository.find_by_id_raw(id_sale)
            if existing is None:
                raise Exception(f'No se encontró la venta con ID {id_sale}')
            
            return self.repository.delete(id_sale)
        except Exception as e:
            logger.error(f"Error deleting sale: {e}")
            raise Exception(f'Error al eliminar la venta: {str(e)}')

    def get_payment_methods(self):
        payment_methods = PaymentMethod.get_all()
        return {
            "data": payment_methods,
            "total": len(payment_methods)
        }
