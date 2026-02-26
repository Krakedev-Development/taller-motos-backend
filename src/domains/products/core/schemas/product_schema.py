import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
from entities.product import Product
from exceptions import validation_exception


class ProductSchema:
    """
    Handles validation and transformation of Product data.
    """

    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> Tuple[Optional[Product], Optional[str]]:
        try:
            validated_data = cls._validate_and_convert(data, is_update=False)
            
            product = Product(
                id_product=str(uuid.uuid4()),
                code=validated_data["code"],
                name=validated_data["name"],
                description=validated_data["description"],
                price=validated_data["price"],
                discount=validated_data.get("discount"),
                stock=validated_data["stock"],
                min_stock=validated_data.get("min_stock", 0),
                max_stock=validated_data.get("max_stock", 0),
                id_supplier=validated_data["id_supplier"],
                id_category=validated_data.get("id_category", ""),
                id_brand=validated_data.get("id_brand", ""),
                model=validated_data.get("model", ""),
                active=validated_data.get("active", True),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            return product, None
        except validation_exception.ValidationException as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error inesperado al validar producto: {str(e)}"

    @classmethod
    def validate_update(cls, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        if not data:
            return None, "Se debe proporcionar al menos un campo para actualizar"
        try:
            validated_data = cls._validate_and_convert(data, is_update=True)
            validated_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            return validated_data, None
        except validation_exception.ValidationException as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error inesperado al validar actualización de producto: {str(e)}"

    @classmethod
    def _validate_and_convert(cls, data: dict, is_update: bool = False) -> dict:
        schema = {
            str: ['code', 'name', 'description', 'id_supplier', 'id_category', 'id_brand', 'model'],
            int: ['stock', 'min_stock', 'max_stock'],
            (int, float): ['price', 'discount'],
            bool: ['active']
        }

        field_rules = {
            'code': {'required': not is_update},
            'name': {'required': not is_update},
            'description': {'required': not is_update},
            'id_supplier': {'required': not is_update},
            'price': {'required': not is_update, 'allow_zero': False},
            'stock': {'required': not is_update, 'allow_zero': True},
            'discount': {'required': False, 'allow_zero': True},
            'min_stock': {'required': False, 'allow_zero': True},
            'max_stock': {'required': False, 'allow_zero': True},
            'id_category': {'required': False},
            'id_brand': {'required': False},
            'model': {'required': False},
            'active': {'required': False}
        }

        validation_exception.validate_fields(data, schema, context="producto", field_rules=field_rules)

        converted = data.copy()
        for field in ['price', 'discount']:
            if field in converted:
                value = converted[field]
                if value is None or value == '':
                    converted[field] = None
                else:
                    try:
                        converted[field] = float(value)
                    except (TypeError, ValueError):
                        raise validation_exception.ValidationException(f"El campo {field} debe ser un número válido")

        cls._validate_business_rules(converted, is_update)
        return converted

    @staticmethod
    def _validate_business_rules(data: dict, is_update: bool):
        min_stock = data.get('min_stock', 0)
        max_stock = data.get('max_stock', 0)
        if min_stock > 0 and max_stock > 0 and min_stock > max_stock:
            raise validation_exception.ValidationException("El stock mínimo no puede ser mayor al stock máximo")

        price = data.get('price')
        if price is not None and price <= 0:
            raise validation_exception.ValidationException("El precio debe ser mayor a 0")

        discount = data.get('discount')
        if discount is not None:
            if discount < 0 or discount > 100:
                raise validation_exception.ValidationException("El descuento debe estar entre 0 y 100")
            if not is_update and discount > 0 and price == 0:
                raise validation_exception.ValidationException("No se puede aplicar un descuento si el precio es 0")
