from app.analytics.repository import AnalyticsRepository


class AnalyticsService:

    def __init__(self):
        self.repo = AnalyticsRepository()

    def get_summary(self):

        return {
            "total_logs": self.repo.get_total_logs(),
            "average_execution_time_ms":
                self.repo.get_average_execution_time(),
            "average_ciphertext_size":
                self.repo.get_average_ciphertext_size(),

            "profile_statistics":
                self.repo.get_selected_profile_stats(),

            "security_statistics":
                self.repo.get_security_rank_stats(),

            "resource_statistics":
                self.repo.get_resource_capability_stats(),

            "hybrid_statistics":
                self.repo.get_hybrid_enabled_stats(),
        }
