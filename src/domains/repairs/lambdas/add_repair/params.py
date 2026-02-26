from core.schemas.repair_schema import RepairSchema
from utils.response_utils import ResponseUtils


def get_params(event) -> dict:
    """
    Loads and validates repair parameters from the event using Domain Schema.
    """
    print("Begin get_params")

    # Handle multipart or JSON
    data, error = RepairSchema.format_multipart_data(event)
    
    if error:
        return ResponseUtils.bad_request_response(error)

    # Validate repair structure and business rules
    repair_data, error = RepairSchema.validate_create(data)
    
    if error:
        return ResponseUtils.bad_request_response(error)

    return repair_data
