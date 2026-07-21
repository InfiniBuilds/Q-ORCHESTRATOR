from app.analytics.repository import AnalyticsRepository

repo = AnalyticsRepository()

print("=" * 50)

print("Total Logs:")
print(repo.get_total_logs())

print()

print("Average Execution Time:")
print(repo.get_average_execution_time())

print()

print("Average Ciphertext Size:")
print(repo.get_average_ciphertext_size())

print()

print("Selected Profile Statistics:")
print(repo.get_selected_profile_stats())

print()

print("Security Rank Statistics:")
print(repo.get_security_rank_stats())

print()

print("Resource Capability Statistics:")
print(repo.get_resource_capability_stats())

print()

print("Hybrid Enabled Statistics:")
print(repo.get_hybrid_enabled_stats())

print("=" * 50)
