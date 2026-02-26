from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
from exceptions.validation_exception import ValidationException
from utils.uuid_generator import generate_uuid_hex, generate_short_numeric
from entities.payment_method import PaymentMethod
from exceptions import validation_exception


class SaleSchema:
    """
    Handles validation and transformation of Sale data.
    """

    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> Tuple[Optional[dict], Optional[str]]:
        try:
            # Main fields validation
            required_fields = {
                str: ['id_customer', 'id_seller', 'payment_method'],
                list: ['products'],
                (float, int): ['subtotal', 'total'],
            }

            validation_exception.validate_fields(data, required_fields)
            
            # Business rules: total vs subtotal
            if float(data["total"]) < float(data["subtotal"]):
                return None, "El campo 'total' no puede ser menor que 'subtotal'"

            # Payment method validation
            payment_method = data.get("payment_method", "").lower()
            if not PaymentMethod.is_valid(payment_method):
                valid_methods = ', '.join(PaymentMethod.get_values())
                return None, f"El campo 'payment_method' debe ser uno de: {valid_methods}"

            # Products validation
            product_fields = {
                str: ['id_product'],
                int: ['quantity', 'stock'],
                (float, int): ['unit_price', 'discount']
            }
            field_rules = {"discount": {"allow_zero": True}}

            products = data["products"]
            for idx, product in enumerate(products, start=1):
                if not isinstance(product, dict):
                    return None, f"Cada producto debe ser un objeto válido (error en producto {idx})"
                validation_exception.validate_fields(product, product_fields, context="products", field_rules=field_rules)
                
                # Stock check
                if product["stock"] < product["quantity"]:
                    return None, f"El stock del producto con codigo {product['id_product']} no puede ser menor a 0"

            # Transformation logic
            id_sale = generate_uuid_hex()
            subtotal = float(data["subtotal"])
            total = float(data["total"])
            
            sale = {
                "id_sale": id_sale,
                "invoice_number": generate_short_numeric(),
                "id_customer": data["id_customer"],
                "id_seller": data["id_seller"],
                "tax": subtotal * 0.15,
                "subtotal": subtotal,
                "total": total,
                "status": data.get("status", "pending"),
                "notes": data.get("notes"),
                "payment_method": payment_method
            }

            details = []
            for product in data["products"]:
                quantity = int(product["quantity"])
                unit_price = float(product["unit_price"])
                discount = float(product.get("discount", 0))
                subtotal_product = (unit_price * quantity) - discount

                sale_detail = {
                    "id_sale_detail": generate_uuid_hex(),
                    "id_sale": id_sale,
                    "id_product": product["id_product"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount": discount,
                    "subtotal": subtotal_product,
                }
                details.append(sale_detail)

            return {
                "sale_data": sale,
                "details_data": details,
            }, None

        except ValidationException as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error inesperado al validar venta: {str(e)}"

    @classmethod
    def validate_update(cls, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        if not data:
            return None, "Se debe proporcionar al menos un campo para actualizar"

        allowed_fields = ["status", "payment_method"]
        update_data = {}
        
        for field in allowed_fields:
            if field in data:
                if field == "payment_method":
                    pm = data[field].lower() if isinstance(data[field], str) else data[field]
                    if not PaymentMethod.is_valid(pm):
                        valid_methods = ', '.join(PaymentMethod.get_values())
                        return None, f"El campo 'payment_method' debe ser uno de: {valid_methods}"
                    update_data[field] = pm
                else:
                    update_data[field] = data[field]

        if not update_data:
            return None, "No se proporcionaron campos válidos para actualizar"

        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        return update_data, None
