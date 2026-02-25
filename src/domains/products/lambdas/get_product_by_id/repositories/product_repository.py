

class ProductRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_by_id(self, id: str):
        response = self.db_client.table('products').select("*").eq("id_product", id).maybe_single().execute()
        print(f"Respuesta de BD: {response}")

        return response.data if response else None

