import base64
import json
import re
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from requests_toolbelt.multipart import decoder
from exceptions import validation_exception
from utils.uuid_generator import generate_uuid_hex, generate_short_numeric


class RepairSchema:
    """
    Handles validation and transformation of Repair data.
    """

    @classmethod
    def format_multipart_data(cls, event: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Handles multipart/form-data decoding."""
        headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
        content_type = headers.get("content-type", "")
        body = event.get("body")

        if body is None:
            return None, "Se debe proporcionar el cuerpo de la petición"

        if event.get("isBase64Encoded", False):
            body_bytes = base64.b64decode(body)
        else:
            body_bytes = body if isinstance(body, (bytes, bytearray)) else body.encode()

        result = {}
        photos = []

        if "multipart/form-data" in content_type.lower():
            try:
                multipart_data = decoder.MultipartDecoder(body_bytes, content_type)
                for part in multipart_data.parts:
                    disposition = part.headers.get(b"Content-Disposition", b"").decode(errors="ignore")
                    name_match = re.search(r'name="([^"]+)"', disposition) or re.search(r'name=([^;]+)', disposition)
                    part_name = name_match.group(1).strip('" ') if name_match else None
                    filename_match = re.search(r'filename="([^"]+)"', disposition)
                    filename = filename_match.group(1) if filename_match else None

                    if part_name in ("payload", "body"):
                        payload = json.loads(part.content.decode("utf-8"))
                        result.update(payload)
                    elif part_name == "photos" or filename:
                        photos.append({"filename": filename, "content": part.content})
            except Exception as e:
                return None, f"Error al procesar multipart-data: {str(e)}"
        else:
            try:
                result = json.loads(body_bytes.decode("utf-8"))
            except Exception as e:
                return None, f"Error al procesar JSON: {str(e)}"

        if photos:
            result["photos"] = photos
        return result, None

    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            # Main structure validation
            required_sections = {dict: ["repair", "vehicle", "labor"], list: ["products"]}
            validation_exception.validate_fields(data, required_sections)

            # Sub-sections validation
            cls._validate_subsections(data)

            # Transformation
            id_vehicle = data["vehicle"].get("id_vehicle", generate_uuid_hex())
            id_repair = generate_uuid_hex()
            
            vehicle = {
                "id_vehicle": id_vehicle,
                "id_customer": data["vehicle"]["id_customer"],
                "license_plate": data["vehicle"]["license_plate"],
                "brand": data["vehicle"]["brand"],
                "model": data["vehicle"]["model"],
                "year": data["vehicle"]["year"],
                "color": data["vehicle"]["color"],
                "mileage": data["vehicle"]["mileage"],
                "active": True
            }

            repair = {
                "id_repair": id_repair,
                "order_number": generate_short_numeric(),
                "id_vehicle": id_vehicle,
                "id_mechanic": data["repair"]["id_mechanic"],
                "fault_description": data["repair"]["fault_description"],
                "diagnosis": data["repair"]["diagnosis"],
                "status": data["repair"]["status"],
                "priority": data["repair"]["priority"],
                "entry_date": data["repair"]["entry_date"],
                "start_date": data["labor"]["start_date"],
                "completion_date": data["labor"]["completion_date"],
                "delivery_date": data["repair"]["delivery_date"],
                "notes": data["repair"]["notes"],
                "estimated_cost": data["repair"]["estimated_cost"],
                "final_cost": data["repair"]["final_cost"],
                "id_created_by": data["repair"]["id_created_by"],
            }

            labor = {
                "id_repair_service": generate_uuid_hex(),
                "id_repair": id_repair,
                **data["labor"]
            }

            materials = []
            for product in data["products"]:
                materials.append({
                    "id_repair_material": generate_uuid_hex(),
                    "id_vehicle": id_vehicle,
                    **product,
                })

            repair_data = {
                "repair": repair,
                "vehicle": vehicle,
                "labor": labor,
                "materials": materials,
            }

            if data.get("photos"):
                repair_data["photos"] = data["photos"]

            return repair_data, None

        except validation_exception.ValidationException as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error inesperado al validar reparación: {str(e)}"

    @classmethod
    def validate_update(cls, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        if not data:
            return None, "Se debe proporcionar al menos un campo para actualizar"

        allowed_fields = [
            "id_mechanic", "fault_description", "diagnosis", 
            "status", "priority", "notes", "estimated_cost", "final_cost"
        ]

        update_data = {}
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]

        if not update_data:
            return None, "No se proporcionaron campos válidos para actualizar"

        # Basic validations for update fields
        if "status" in update_data:
            valid_statuses = ["EN_PROCESO", "PENDIENTE", "TERMINADA", "CANCELADA"]
            if update_data["status"] not in valid_statuses:
                return None, f"El estado debe ser uno de: {', '.join(valid_statuses)}"

        if "priority" in update_data:
            valid_priorities = ["BAJA", "MEDIA", "ALTA", "URGENTE"]
            if update_data["priority"] not in valid_priorities:
                return None, f"La prioridad debe ser una de: {', '.join(valid_priorities)}"

        # Add updated_at
        from datetime import timezone
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        return update_data, None

    @staticmethod
    def _validate_subsections(data: dict):
        # Vehicle
        vehicle_fields = {str: ["id_customer", "license_plate", "brand", "model", "color"], int: ["year", "mileage"]}
        validation_exception.validate_fields(data["vehicle"], vehicle_fields)

        # Repair
        repair_fields = {
            str: ["id_mechanic", "fault_description", "diagnosis", "status", "priority", "notes", "id_created_by"],
            datetime: ["entry_date", "delivery_date"],
            float: ["estimated_cost", "final_cost"]
        }
        validation_exception.validate_fields(data["repair"], repair_fields)

        # Labor
        labor_fields = {str: ["id_service_type"], datetime: ["start_date", "completion_date"], int: ["actual_hours"], float: ["agreed_price"], bool: ["completed"]}
        validation_exception.validate_fields(data["labor"], labor_fields)

        # Products
        product_fields = {str: ['id_product'], int: ['quantity', 'stock'], float: ['unit_price', 'discount']}
        for idx, product in enumerate(data["products"], start=1):
            if not isinstance(product, dict):
                raise ValueError(f"Cada producto debe ser un objeto válido (error en producto {idx})")
            validation_exception.validate_fields(product, product_fields, context="products", field_rules={"discount": {"allow_zero": True}})
