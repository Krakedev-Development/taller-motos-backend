import json
from datetime import datetime, timezone
from exceptions import validation_exception


def load_update_parameters(event):
    print(f'Begin load_update_parameters')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcionar el ID del proveedor en la ruta"
            })
        }

    id_product = path_parameters['id']
    if not id_product or id_product.strip() == '':
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "El ID del proveedor no puede estar vacío"
            })
        }

    request_body = event.get('body', None)
    if request_body is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcionar el cuerpo de la petición"
            })
        }

    try:
        request_body = json.loads(request_body)
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "El cuerpo de la petición debe ser un JSON válido"
            })
        }

    print(f'request_body: {request_body}')

    if not request_body:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcionar al menos un campo para actualizar"
            })
        }

    validated_data = validate_and_convert_update_fields(request_body)

    validated_data['updated_at'] = datetime.now(timezone.utc).isoformat()

    return id_product, validated_data


def validate_and_convert_update_fields(data: dict) -> dict:
    """
    Validates and converts product update field data types.
    All fields are optional for updates.
    """
    schema = {
        str: ['code', 'name', 'description', 'id_supplier', 'id_category', 'id_brand', 'model'],
        int: ['stock', 'min_stock', 'max_stock'],
        (int, float): ['price', 'discount'],
        bool: ['active']
    }

    field_rules = {
        'code': {'required': False},
        'name': {'required': False},
        'description': {'required': False},
        'id_supplier': {'required': False},
        'price': {'required': False, 'allow_zero': False},
        'stock': {'required': False, 'allow_zero': True},
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
                    raise validation_exception.ValidationException(
                        f"El campo {field} debe ser un número válido"
                    )

    validate_update_business_rules(converted)

    return converted


def validate_update_business_rules(data: dict):
    """
    Applies custom business rules for product update validation.
    """
    if 'min_stock' in data and 'max_stock' in data:
        min_stock = data.get('min_stock', 0)
        max_stock = data.get('max_stock', 0)
        if min_stock > 0 and 0 < max_stock < min_stock:
            raise validation_exception.ValidationException(
                "El stock mínimo no puede ser mayor al stock máximo"
            )

    if 'price' in data:
        price = data.get('price')
        if price is not None and price <= 0:
            raise validation_exception.ValidationException(
                "El precio debe ser mayor a 0"
            )

    if 'discount' in data:
        discount = data.get('discount')
        if discount is not None:
            if discount < 0 or discount > 100:
                raise validation_exception.ValidationException(
                    "El descuento debe estar entre 0 y 100"
                )