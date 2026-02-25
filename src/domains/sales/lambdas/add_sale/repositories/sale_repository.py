from supabase import Client


class SaleRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def save(self, sale_data: dict) -> dict:
        print(f'Data de venta para guardar: {sale_data}')
        response = self.db_client.rpc("insert_sale_with_details", sale_data).execute()
        print(f"Respuesta de insersion de venta: {response}")
        return response.data if response.data else None

    def delete(self, sale_id: int):
        self.db_client.table("sales").delete().eq("id_sale", sale_id).execute()
