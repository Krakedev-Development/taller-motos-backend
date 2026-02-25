import math
import logging

from repositories.sale_repository import SaleRepository

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SaleUseCase:
    def __init__(self, repository: SaleRepository):
        self.repository = repository
        logger.info('SaleUseCase initialized')

    def get_sales(self, page=1, limit=10, search=None, record_type=None, payment_method=None):
        logger.info(f'=== SaleUseCase.get_sales CALLED ===')
        logger.info(f'Input parameters: page={page}, limit={limit}, search={search}, record_type={record_type}, payment_method={payment_method}')
        
        try:
            pm = payment_method
            if isinstance(pm, str) and pm.strip().lower() in ("", "null"):
                logger.info(f'Normalizing payment_method: "{payment_method}" -> None')
                pm = None
            else:
                logger.info(f'Payment method after normalization: {pm}')

            logger.info(f'Calling repository.find_all with: page={page}, limit={limit}, search={search}, record_type={record_type}, pm={pm}')
            data, total = self.repository.find_all(page, limit, search, record_type, pm)
            logger.info(f'Repository returned: {len(data)} items, total={total}')
            
            totalPages = math.ceil(total / limit) if limit > 0 else 0
            logger.info(f'Calculated totalPages: {totalPages}')
            
            result = {
                "data": data,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "totalPages": totalPages
                },
            }
            logger.info(f'=== SaleUseCase.get_sales COMPLETED SUCCESSFULLY ===')
            return result
        
        except Exception as e:
            logger.error(f'ERROR in SaleUseCase.get_sales: {type(e).__name__}: {str(e)}', exc_info=True)
            raise
