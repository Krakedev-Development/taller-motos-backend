from typing import Dict, Any
from repositories.dashboard_repository import DashboardRepository


class DashboardUseCase:
    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    def get_dashboard_data(self, code: str = None) -> Dict[str, Any]:
        """
        Obtiene los datos resumidos para el dashboard
        
        Args:
            code: Tipo de dashboard ('SELLER' para vendedor, None para admin)
        
        Returns:
            dict: Diccionario con los datos del dashboard
        """
        if code and code.upper() == "SELLER":
            return self._get_seller_dashboard()
        
        return self._get_admin_dashboard()
    
    def _get_admin_dashboard(self) -> Dict[str, Any]:
        """Dashboard para administradores"""
        summary = self.repository.get_summary()
        
        return {
            "total_products": int(summary.get("total_products", 0)),
            "pending_repairs": int(summary.get("pending_repairs", 0)),
            "monthly_sales": float(summary.get("monthly_sales", 0.0)),
            "low_stock": int(summary.get("low_stock", 0)),
            "lowest_stock_product_name": summary.get("lowest_stock_product_name", ""),
            "lowest_stock_product_quantity": int(summary.get("lowest_stock_product_quantity", 0))
        }
    
    def _get_seller_dashboard(self) -> Dict[str, Any]:
        """Dashboard para vendedores"""
        summary = self.repository.get_summary_seller()
        
        return {
            "daily_sales": float(summary.get("daily_sales", 0.0)),
            "pending_repairs": int(summary.get("pending_repairs", 0)),
            "total_customers": int(summary.get("total_customers", 0)),
            "total_products": int(summary.get("total_products", 0))
        }