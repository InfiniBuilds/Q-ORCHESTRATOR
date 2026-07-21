from pprint import pprint

from app.analytics.service import AnalyticsService

service = AnalyticsService()

pprint(service.get_summary())
