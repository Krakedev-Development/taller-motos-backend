import logging
from typing import List, Tuple, Optional, Any
from supabase import Client

logger = logging.getLogger(__name__)

class SaleRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: Optional[str] = None, 
                 record_type: Optional[str] = None, payment_method: Optional[str] = None) -> Tuple[List[dict], int]:
        try:
            offset = (page - 1) * limit
            rpc_params = {
                "p_id_sale": None,
                "p_search": search,
                "p_limit": limit,
                "p_offset": offset,
                "p_record_type": record_type,
                "p_payment_method": payment_method
            }
            
            response = self.db_client.rpc("get_sales_cpr", rpc_params).execute()
            
            # The get_sales_cpr RPC seems to return a dict with "data" and "total" in some versions,
            # but looking at get_sales/repositories/sale_repository.py, it does response.data.get("data", [])
            if isinstance(response.data, dict):
                data = response.data.get("data", [])
                total = response.data.get("total", 0)
            else:
                data = response.data or []
                total = len(data) # Fallback if RPC doesn't return count
                
            return data, total
        except Exception as e:
            logger.error(f'Error in SaleRepository.find_all: {str(e)}')
            raise

    def find_by_id(self, id_sale: str) -> Optional[dict]:
        try:
            response = self.db_client.rpc("get_sales_cpr", {
                "p_id_sale": id_sale,
                "p_search": None,
                "p_limit": None,
                "p_offset": None,
                "p_record_type": None,
                "p_payment_method": None
            }).execute()

            if not response.data:
                return None

            # If it's the RPC result, it might be in a list or a dict
            if isinstance(response.data, list):
                return response.data[0] if response.data else None
            elif isinstance(response.data, dict) and "data" in response.data:
                data_list = response.data["data"]
                return data_list[0] if data_list else None
                
            return response.data
        except Exception as e:
            logger.error(f"Error al buscar la venta por ID: {str(e)}")
            raise

    def find_by_id_raw(self, id_sale: str) -> Optional[dict]:
        """Direct table table query to find a sale, used for updates (e.g. check if it's a quote)"""
        try:
            response = self.db_client.table('sales').select("*").eq("id_sale", id_sale).maybe_single().execute()
            return response.data if response else None
        except Exception as e:
            logger.error(f"Error in find_by_id_raw: {e}")
            raise

    def save_transaction(self, sale_data: dict) -> Optional[dict]:
        try:
            response = self.db_client.rpc("insert_sale_with_details", sale_data).execute()
            return response.data if response.data else None
        except Exception as e:
            logger.error(f"Error al guardar la venta: {e}")
            raise Exception(f"No se pudo guardar la venta: {e}")

    def update(self, id_sale: str, update_data: dict) -> List[dict]:
        try:
            response = self.db_client.table("sales") \
                .update(update_data) \
                .eq('id_sale', id_sale) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró la venta con ID {id_sale}')

            return response.data
        except Exception as e:
            logger.error(f'Error al actualizar la venta: {e}')
            raise

    def delete(self, id_sale: str) -> List[dict]:
        try:
            # Delete details first if not handled by CASCADE
            self.db_client.table("sale_details").delete().eq("id_sale", id_sale).execute()
            
            response = self.db_client.table("sales") \
                .delete() \
                .eq('id_sale', id_sale) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró la venta con ID {id_sale}')

            return response.data
        except Exception as e:
            logger.error(f'Error al eliminar la venta: {e}')
            raise

    def update_product_stock(self, id_product: int, stock: int):
        try:
            self.db_client.table("products").update({"stock": stock}).eq("id_product", id_product).execute()
        except Exception as e:
            logger.error(f"Error updating product stock: {e}")
            raise
