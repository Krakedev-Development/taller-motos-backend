import json

from exceptions import validation_exception
from exceptions.validation_exception import ValidationException
from utils.uuid_generator import generate_uuid_hex, generate_short_numeric
from entities.payment_method import PaymentMethod


def load_initial_parameters(event):
    print(f'Begin load_initial_parameters')
    print(f'Event: {event}')

    request_body = event.get('body', None)
    if request_body is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcionar el cuerpo de la petición"
            })
        }

    request_body = json.loads(request_body)
    print(f'request_body: {request_body}')
    validate_fields(request_body)
    sale_date = generate_sale_data(request_body)
    return sale_date


def validate_fields(request_body: dict):
    print("Begin validate_fields")

    required_fields = {
        str: ['id_customer', 'id_seller', 'payment_method'],
        list: ['products'],
        float: ['subtotal', 'total'],
    }

    validation_exception.validate_fields(request_body, required_fields,
                                         extra_validations=[total_greater_equal_subtotal, validate_payment_method])

    product_fields = {
        str: ['id_product'],
        int: ['quantity', 'stock'],
        float: ['unit_price', 'discount']
    }

    field_rules = {
        "discount": {"allow_zero": True},
    }

    products = request_body["products"]
    for idx, product in enumerate(products, start=1):

        if not isinstance(product, dict):
            raise ValueError(f"Cada producto debe ser un objeto válido (error en producto

        validation_exception.validate_fields(product, product_fields, context="products", field_rules=field_rules)


def total_greater_equal_subtotal(data):
    if data["total"] < data["subtotal"]:
        raise ValidationException("El campo 'total' no puede ser menor que 'subtotal'")


def validate_payment_method(data):
    """Valida que el método de pago sea uno de los permitidos"""
    payment_method = data.get("payment_method", "").lower()
    
    if not PaymentMethod.is_valid(payment_method):
        valid_methods = ', '.join(PaymentMethod.get_values())
        raise ValidationException(
            f"El campo 'payment_method' debe ser uno de: {valid_methods}"
        )


def generate_sale_data(request_body: dict) -> dict:
    print(f"Begin generate_sale_data")
    id_sale = generate_uuid_hex()
    subtotal = float(request_body["subtotal"])
    total = float(request_body["total"])
    status = request_body["status"] if "status" in request_body else "pending"
    notes = request_body["notes"] if "notes" in request_body else None
    payment_method = request_body["payment_method"].lower()

    sale = {
        "id_sale": id_sale,
        "invoice_number": generate_short_numeric(),
        "id_customer": request_body["id_customer"],
        "id_seller": request_body["id_seller"],
        "tax": subtotal * 0.15,
        "subtotal": subtotal,
        "total": total,
        "status": status,
        "notes": notes,
        "payment_method": payment_method
    }

    details = []

    for product in request_body["products"]:
        quantity = int(product["quantity"])
        unit_price = float(product["unit_price"])
        discount = float(product.get("discount", 0))
        subtotal_product = (unit_price * quantity) - discount

        updated_stock = product["stock"] - product["quantity"]
        if updated_stock < 0:
            raise ValidationException(
                f"El stock del producto con codigo {product['id_product']} no puede ser menor a 0")

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
    }
