from app.database import database_logger
from app.logging.mapper import OrchestrationMapper


class OrchestrationLogger:

    def log(
        self,
        context,
        result,
        execution_time_ms: float,
    ):

        database_model = (
            OrchestrationMapper.to_database_model(
                context=context,
                result=result,
                execution_time_ms=execution_time_ms,
            )
        )

        database_logger.log(database_model)
