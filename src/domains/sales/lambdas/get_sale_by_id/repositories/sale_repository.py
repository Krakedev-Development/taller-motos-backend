from supabase import Client


class SaleRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id_sale: str):
        """
        Busca una venta por ID.
        """
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

            return response.data
        except Exception as e:
            print(f"Error al buscar la venta: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el venta: {str(e)}')

