import uuid
from typing import Dict, Any, Tuple, Optional, List
from entities.product import Product
from exceptions import validation_exception


class BulkProductSchema:
    """
    Handles validation and transformation of Bulk Product data.
    """

    @classmethod
    def validate_create(cls, data: Any) -> Tuple[Optional[Dict[str, List[dict]]], Optional[str]]:
        if not isinstance(data, list):
            return None, "El cuerpo de la petición debe ser una lista de productos"
            
        if len(data) == 0:
            return None, "Se debe proporcionar al menos un producto"

        required_fields = {
            str: ['code', 'name', 'description', 'id_supplier', 'id_category', 'id_brand'],
            int: ['stock', 'min_stock', 'max_stock'],
            (float, int): ['price'],
            bool: ['active']
        }

        try:
            products = []
            for idx, product_data in enumerate(data, start=1):
                if not isinstance(product_data, dict):
                    return None, f"Cada producto debe ser un objeto válido (error en producto {idx})"
                
                validation_exception.validate_fields(product_data, required_fields, context="products")
                
                # Transform to entity then to dict for repository
                product_entity = Product.from_dict(product_data)
                if not product_entity.id_product:
                    product_entity.id_product = str(uuid.uuid4())
                    
                products.append(product_entity.to_dict())

            return {"products_data": products}, None
            
        except validation_exception.ValidationException as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error inesperado al validar carga masiva: {str(e)}"
