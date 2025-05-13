from Lista8.HttpLog import HttpLog
from Lista8.helpers import get_logger


class LogLoader:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logs = []


    def __len__(self) -> int:
        return len(self.logs)

    def load_logs(self, filename):
        try:
            with open(filename, 'r') as file:
                raw_logs = file.readlines()
                for log in raw_logs:
                    try:
                        self.logs.append(HttpLog(log.strip()))
                    except Exception as e:
                        self.logger.error(f"Błąd wczytywania logu: {log.strip()} | Błąd: {e}")
        except Exception as e:
            self.logger.error(f"Błąd wczytywania pliku: {e}")
            raise

    def get_all_logs(self):
        return self.logs

    def get_filtered_logs(self, start_date, end_date):
        return [log for log in self.logs if start_date <= log.timestamp <= end_date]
