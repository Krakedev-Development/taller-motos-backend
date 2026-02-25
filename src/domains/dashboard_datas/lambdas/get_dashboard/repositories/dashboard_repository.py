from typing import Dict, Any


class DashboardRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def get_summary(self) -> Dict[str, Any]:
        """
        Obtiene los datos del dashboard desde la vista dashboard_summary
        
        La vista contiene:
        - total_products: Total de productos activos
        - pending_repairs: Reparaciones pendientes
        - monthly_sales: Ventas del mes actual (solo pagadas)
        - low_stock: Productos con stock bajo (< 10 unidades)
        
        Returns:
            dict: Diccionario con los datos del dashboard
        """
        try:
            response = self.db_client.table("dashboard_summary").select("*").single().execute()
            
            if not response.data:
                return {
                    "total_products": 0,
                    "pending_repairs": 0,
                    "monthly_sales": 0.0,
                    "low_stock": 0,
                    "lowest_stock_product_name": "" ,
                    "lowest_stock_product_quantity": 0
                }
            
            return response.data
            
        except Exception as e:
            print(f"Error al obtener datos del dashboard: {str(e)}")
            raise Exception(f"Error al consultar la vista del dashboard: {str(e)}")

    def get_summary_seller(self) -> Dict[str, Any]:
        """
        Obtiene los datos del dashboard desde la vista dashboard_summary
        
        La vista contiene:
        - total_products: Total de productos activos
        - pending_repairs: Reparaciones pendientes
        - monthly_sales: Ventas del mes actual (solo pagadas)
        - low_stock: Productos con stock bajo (< 10 unidades)
        
        Returns:
            dict: Diccionario con los datos del dashboard
        """
        try:
            response = self.db_client.table("dashboard_summary_seller").select("*").single().execute()
            
            if not response.data:
                return {
                    "daily_sales": 0,
                    "pending_repairs": 0,
                    "total_customers": 0,
                    "total_products": 0
                }
            
            return response.data
            
        except Exception as e:
            print(f"Error al obtener datos del dashboard: {str(e)}")
            raise Exception(f"Error al consultar la vista del dashboard: {str(e)}")

