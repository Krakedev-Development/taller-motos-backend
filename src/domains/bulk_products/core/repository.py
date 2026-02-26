from supabase import Client


class BulkProductRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def bulk_save(self, products_data: dict) -> dict:
        """
        Inserts multiple products using the 'bulk_insert_products' RPC.
        """
        try:
            response = self.db_client.rpc('bulk_insert_products', products_data).execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Error in BulkProductRepository.bulk_save: {str(e)}")
            raise Exception(f"Error al realizar la carga masiva: {str(e)}")
