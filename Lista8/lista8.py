# Tworzenie instancji LogLoader
from datetime import datetime

from Lista8.LogLoader import LogLoader

log_loader = LogLoader()

log_loader.load_logs("logs.log")

logs = log_loader.get_all_logs()

start_date = datetime(2025, 5, 1)
end_date = datetime(2025, 5, 8)
filtered_logs = log_loader.get_filtered_logs(start_date, end_date)

