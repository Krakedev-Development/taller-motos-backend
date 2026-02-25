from supabase import Client
from entities.supplier import Supplier

class SupplierRepository:
    def __init__(self, db_client : Client):
        self.db_client = db_client
    
    def save(self, supplier: Supplier):
        """Método para guardar un nuevo proveedor en la base de datos"""
        data = supplier.to_dict()
        try:
            response = self.db_client.table("suppliers").insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error al guardar el proveedor: {str(e)}")
            raise Exception("Error al guardar el proveedor")
