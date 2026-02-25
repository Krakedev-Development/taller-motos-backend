from repositories.brand_repository import BrandRepository
import math

class BrandUseCase:
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def get_brands(self, page=1, limit=1000, type_brand=None):
        data, total = self.repository.find_all(page, limit, type_brand)
        totalPages = math.ceil(total / limit) if limit > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": totalPages
            }
        }
