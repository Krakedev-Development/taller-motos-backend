import json
import uuid
from datetime import datetime, timezone
from entities.mechanic import Mechanic
from utils.response_utils import ResponseUtils  

def load_initial_parameters(event):
    body = event.get("body")
    if not body:
        return ResponseUtils.bad_request_response("El cuerpo de la petición es obligatorio")
    
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("El cuerpo de la petición no tiene un formato JSON válido")

    for field in ["id_number", "name"]:
        if not data.get(field):
            return ResponseUtils.bad_request_response(f"El campo {field} es obligatorio")

    now = datetime.now(timezone.utc).isoformat()

    mechanic = Mechanic(
        id_mechanic=str(uuid.uuid4()),
        id_number=data["id_number"],
        name=data["name"],
        surname=data.get("surname"),
        phone=data.get("phone"),
        email=data.get("email"),
        address=data.get("address"),
        hire_date=data.get("hire_date"),
        salary=data.get("salary"),
        active=data.get("active", True),
        created_at=now,
        updated_at=now
    )

    return mechanic
