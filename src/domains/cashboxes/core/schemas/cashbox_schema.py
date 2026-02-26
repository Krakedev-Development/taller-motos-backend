import uuid
from typing import Dict, Any, Tuple, Optional
from entities.cashbox import Cashbox


class CashboxSchema:
    """
    Handles validation and transformation of Cashbox data.
    """

    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> Tuple[Optional[Cashbox], Optional[str]]:
        required_fields = ["type", "amount", "id_user", "concept"]
        for field in required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == "":
                return None, f"El campo '{field}' es obligatorio"

        translations = {
            "INGRESO": "INCOME", "EGRESO": "EXPENSE", "AJUSTE": "ADJUSTMENT",
            "INCOME": "INCOME", "EXPENSE": "EXPENSE", "ADJUSTMENT": "ADJUSTMENT"
        }

        type_normalized = str(data["type"]).strip().upper()
        movement_type = translations.get(type_normalized)

        if not movement_type:
            return None, "El campo 'type' debe ser 'INCOME'/'INGRESO', 'EXPENSE'/'EGRESO' o 'ADJUSTMENT'/'AJUSTE'"

        try:
            amount = float(data["amount"])
            if amount <= 0:
                return None, "El monto debe ser mayor a 0"
        except (ValueError, TypeError):
            return None, "El monto debe ser un número válido"

        concept = str(data["concept"]).strip()
        if not concept:
            return None, "El concepto no puede estar vacío"

        cashbox = Cashbox(
            id_cashbox=str(uuid.uuid4()),
            id_user=data["id_user"],
            id_session=None,
            type=movement_type,
            concept=concept,
            amount=amount,
            id_sale=data.get("id_sale")
        )

        return cashbox, None
