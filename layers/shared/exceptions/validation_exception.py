from datetime import datetime
from typing import Dict, Any, List, Type, Callable, Union


class ValidationException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


def validate_fields(
        data: Dict[str, Any],
        schema: Dict[Union[Type, tuple], List[str]],
        context: str = "",
        extra_validations: List[Callable[[Dict[str, Any]], None]] = None,
        field_rules: Dict[str, Dict[str, Any]] = None
):
    field_rules = field_rules or {}

    for expected_type, fields in schema.items():
        for field in fields:
            value = data.get(field, None)

            rules = field_rules.get(field, {})

            required = rules.get("required", True)
            if required and value in (None, "", [], {}):
                raise ValidationException(
                    f"El campo '{field}' {f'en {context}' if context else ''} es obligatorio y no puede estar vacío"
                )

            if value in (None, "", [], {}):
                continue

            if isinstance(expected_type, tuple):
                if not isinstance(value, expected_type):
                    type_names = " o ".join([t.__name__ for t in expected_type])
                    raise ValidationException(
                        f"El campo '{field}' {f'en {context}' if context else ''} debe ser de tipo {type_names}"
                    )
                
                if any(t in (int, float) for t in expected_type) and isinstance(value, (int, float)):
                    allow_zero = rules.get("allow_zero", False)
                    if not allow_zero and value <= 0:
                        raise ValidationException(
                            f"El campo '{field}' {f'en {context}' if context else ''} debe ser mayor a 0"
                        )
                    if allow_zero and value < 0:
                        raise ValidationException(
                            f"El campo '{field}' {f'en {context}' if context else ''} no puede ser negativo"
                        )
                continue


            if expected_type in (int, float):
                allow_zero = rules.get("allow_zero", False)
                if not allow_zero and value <= 0:
                    raise ValidationException(
                        f"El campo '{field}' {f'en {context}' if context else ''} debe ser mayor a 0"
                    )
                if allow_zero and value < 0:
                    raise ValidationException(
                        f"El campo '{field}' {f'en {context}' if context else ''} no puede ser negativo"
                    )

            if expected_type is str:
                if not (1 <= len(value) <= 255):
                    raise ValidationException(
                        f"El campo '{field}' {f'en {context}' if context else ''} debe tener entre 1 y 255 caracteres")


    if extra_validations:
        for validation_func in extra_validations:
            validation_func(data)
