import json
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters
from repositories.repair_repository import RepairRepository
from repositories.storage_repository import StorageRepository
from repositories.vehicle_repository import VehicleRepository
from use_cases.repair_use_case import RepairUseCase
from use_cases.save_images_use_case import SaveImagesUseCase

db_client = DBClient.get_client()
repair_repository = RepairRepository(db_client)
vehicle_repository = VehicleRepository(db_client)
repair_use_case = RepairUseCase(repair_repository)
storage_repository = StorageRepository(db_client, "repairs-images")
image_use_case = SaveImagesUseCase(storage_repository)

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        repair_data = load_initial_parameters(event)

        if isinstance(repair_data, dict) and "statusCode" in repair_data:
            return repair_data


        result = repair_use_case.execute(repair_data)
        
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        print(f'Error al registrar la reparación: {e}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
