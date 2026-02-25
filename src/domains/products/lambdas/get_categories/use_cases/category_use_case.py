from repositories.category_repository import CategoryRepository
import math

class CategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def get_categories(self, page=1, limit=1000):
        data, total = self.repository.find_all(page, limit)
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
