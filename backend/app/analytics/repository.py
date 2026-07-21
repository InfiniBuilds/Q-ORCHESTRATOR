from sqlalchemy import func

from app.database.models import OrchestrationLog
from app.database.session import SessionLocal


class AnalyticsRepository:
    def get_total_logs(self) -> int:
        with SessionLocal() as session:
            return session.query(func.count(OrchestrationLog.id)).scalar()

    def get_average_execution_time(self) -> float:
        with SessionLocal() as session:
            value = session.query(
                func.avg(OrchestrationLog.execution_time_ms)
            ).scalar()
            return round(value or 0, 3)

    def get_average_ciphertext_size(self) -> float:
        with SessionLocal() as session:
            value = session.query(
                func.avg(OrchestrationLog.ciphertext_size)
            ).scalar()
            return round(value or 0, 2)

    def get_selected_profile_stats(self):
        with SessionLocal() as session:
            rows = (
                session.query(
                    OrchestrationLog.selected_profile,
                    func.count(OrchestrationLog.id),
                )
                .group_by(OrchestrationLog.selected_profile)
                .all()
            )

            return {
                profile: count
                for profile, count in rows
            }

    def get_security_rank_stats(self):
        with SessionLocal() as session:
            rows = (
                session.query(
                    OrchestrationLog.security_rank,
                    func.count(OrchestrationLog.id),
                )
                .group_by(OrchestrationLog.security_rank)
                .all()
            )

            return {
                rank: count
                for rank, count in rows
            }

    def get_resource_capability_stats(self):
        with SessionLocal() as session:
            rows = (
                session.query(
                    OrchestrationLog.resource_capability,
                    func.count(OrchestrationLog.id),
                )
                .group_by(OrchestrationLog.resource_capability)
                .all()
            )

            return {
                capability: count
                for capability, count in rows
            }

    def get_hybrid_enabled_stats(self):
        with SessionLocal() as session:
            rows = (
                session.query(
                    OrchestrationLog.hybrid_enabled,
                    func.count(OrchestrationLog.id),
                )
                .group_by(OrchestrationLog.hybrid_enabled)
                .all()
            )

            return {
                enabled: count
                for enabled, count in rows
            }
