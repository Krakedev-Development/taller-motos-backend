import json
from datetime import datetime, timezone
from entities.product import Product
from exceptions import validation_exception
from utils.uuid_generator import generate_uuid_hex


def load_initial_parameters(event):
    print(f'Begin load_initial_parameters')
    print(f'Event: {event}')

    request_body = event.get('body', None)

    if request_body is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcinar el cuerpo de la peticion"
            })
        }

    request_body = json.loads(request_body)

    print(f'request_body: {request_body}')

    validate_product_fields(request_body)

    products = formatted_products(request_body)

    return products


def validate_product_fields(products: dict):
    if len(products) == 0:
        raise ValueError(f"Se debe proporcionar al menos un producto")

    required_fields = {
        str: ['code', 'name', 'description', 'id_supplier', 'id_category', 'id_brand'],
        int: ['stock', 'min_stock', 'max_stock'],
        float: ['price'],
        bool: ['active']
    }

    for idx, product in enumerate(products, start=1):

        if not isinstance(product, dict):
            raise ValueError(f"Cada producto debe ser un objeto válido (error en producto

        validation_exception.validate_fields(product, required_fields, context="products")


def formatted_products(request_body):
    products = []
    for product in request_body:
        formatted_product = Product.from_dict(product)
        products.append(formatted_product.to_dict())

    return {"products_data": products}
