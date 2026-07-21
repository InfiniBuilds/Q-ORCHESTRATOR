from app.database.models import OrchestrationLog
from app.database.session import SessionLocal


class DatabaseLogger:

    def log(self, log: OrchestrationLog) -> None:

        session = SessionLocal()

        try:
            session.add(log)
            session.commit()

        finally:
            session.close()
