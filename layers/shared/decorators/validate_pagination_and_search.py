from functools import wraps
from utils.response_utils import ResponseUtils

def validate_pagination_and_search(max_limit: int = 100):
    """
    Decorador para endpoints públicos GET con parámetros:
    - page: int (>=1)
    - limit: int (>=1)
    - search: str (opcional, 1-100 caracteres)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                query_params = event.get("queryStringParameters") or {}

                try:
                    page = int(query_params.get("page", 1))
                    limit = int(query_params.get("limit", 10))
                except ValueError:
                    return ResponseUtils.bad_request_response(
                        "Los parámetros 'page' y 'limit' deben ser números enteros válidos"
                    )

                if page < 1:
                    return ResponseUtils.bad_request_response(
                        "El parámetro 'page' debe ser mayor o igual a 1"
                    )
                
                if limit < 1:
                    return ResponseUtils.bad_request_response(
                        "El parámetro 'limit' debe ser mayor o igual a 1"
                    )
                
                if limit > max_limit:
                    limit = max_limit

                search = query_params.get("search", "").strip() if query_params.get("search") else None
                if search:
                    if len(search) > 100:
                        return ResponseUtils.bad_request_response(
                            "El parámetro 'search' no puede tener más de 100 caracteres"
                        )

                event["validated_params"] = {
                    "page": page,
                    "limit": limit,
                    "search": search
                }

                return func(event, context)

            except Exception:
                return ResponseUtils.bad_request_response("Parámetros de paginación inválidos")
        
        return wrapper
    return decorator