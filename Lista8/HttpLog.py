import re

from Lista8.helpers import safe_int, parse_timestamp

# https://stackoverflow.com/questions/9234699/understanding-apaches-access-log

COMBINED_LOG_FORMAT_REGEX = r'(?P<remote_host>\S+) (?P<identity>\S+) (?P<username>\S+) \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<request_line>[^\s]+ \S+)" (?P<status_code>\d+) (?P<response_size>\S+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
REMOTE_HOST = 'remote_host'
IDENTITY = 'identity'
USERNAME = 'username'
TIMESTAMP = 'timestamp'
METHOD = 'method'
REQUEST_LINE = 'request_line'
STATUS_CODE = 'status_code'
RESPONSE_SIZE = 'response_size'
REFERER = 'referer'
USER_AGENT = 'user_agent'

def parse_log(raw_log: str) -> dict:
    match = re.match(COMBINED_LOG_FORMAT_REGEX, raw_log)
    if match:
        return match.groupdict()
    else:
        raise ValueError(f"Log line does not match expected format: {raw_log}")

class HttpLog:
    def __init__(self, raw_log: str) -> None:
        log_data = parse_log(raw_log)
        self.remote_host = log_data.get(REMOTE_HOST)
        self.identity = log_data.get(IDENTITY)
        self.username = log_data.get(USERNAME)
        self.timestamp = parse_timestamp(log_data.get(TIMESTAMP))
        self.timezone = self.timestamp.tzinfo
        self.method = log_data.get(METHOD)
        self.request_line_without_method = log_data.get(REQUEST_LINE)
        self.status_code = safe_int(log_data.get(STATUS_CODE))
        self.response_size = safe_int(log_data.get(RESPONSE_SIZE))
        self.referer = log_data.get(REFERER)
        self.user_agent = log_data.get(USER_AGENT)
        self.raw_log = raw_log

    @property
    def preview(self) -> str:
        return self.preview_by_len()

    def preview_by_len(self, length: int = 30) -> str:
        return self.raw_log[:length] + "..." if len(self.raw_log) > length else self.raw_log
