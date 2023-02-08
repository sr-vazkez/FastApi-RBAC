from datetime import datetime
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Create a custom JSON Format.

    Args:
        jsonlogger (JsonFormatter): Extends JSONFormatter class
    """

    def add_fields(self, log_record, record, message_dict) -> None:
        """Add more fields in the new format.

        Args:
            log_record (Dict[str, Any]): obtain a new key value
            record (LogRecord): To choose logrecord
            message_dict (Dict[str, Any]): Define a specific string
        """
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["@timestamp"] = now
        if log_record.get("log.level"):
            log_record["log.level"] = log_record["log.level"].upper()
        else:
            log_record["log.level"] = record.levelname

        if log_record.get("log.logger"):
            log_record["log.logger"] = log_record["log.logger"].upper()
        else:
            log_record["log.logger"] = record.name
