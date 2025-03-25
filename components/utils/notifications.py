from nicegui import ui
import datetime
from enum import Enum

class LogSeverity(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

def show_notification(message: str, 
                    notification_type: str = "info", 
                    duration: float = 4.0,
                    channel: str = "default"):
    """Display a styled notification with duration control and channel support"""
    ui.notify(
        message,
        type=notification_type,
        timeout=duration * 1000,
        position="bottom-right",
        progress=True,
        channel=channel
    )
    log_activity(f"Notification [{channel}] ({notification_type}): {message}", 
               severity=LogSeverity.INFO)

def log_activity(message: str, 
               severity: LogSeverity = LogSeverity.INFO,
               channel: str = "app"):
    """Centralized logging with timestamp and severity levels"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{channel}] [{severity.value.upper()}]: {message}"
    print(log_entry)

def log_and_notify(message: str,
                 notification_type: str = "info",
                 log_severity: LogSeverity = LogSeverity.INFO,
                 channel: str = "default",
                 duration: float = 4.0):
    """Combined logging and notification with channel support"""
    show_notification(message, notification_type, duration, channel)
    log_activity(f"Notified: {message}", log_severity, channel)

def task_log_and_notify(task_name: str, success: bool = True, error_msg: str = ""):
    """Convenience wrapper for task completion notifications"""
    if success:
        log_and_notify(f"Task completed: {task_name}",
                      notification_type="positive",
                      log_severity=LogSeverity.INFO,
                      channel="tasks")
    else:
        log_and_notify(f"Task failed: {task_name} - {error_msg}",
                      notification_type="negative", 
                      log_severity=LogSeverity.ERROR,
                      channel="errors")

def debug_log(message: str, channel: str = "debug"):
    """Debug logging with caller context"""
    import inspect
    frame = inspect.currentframe().f_back
    file_info = f"{frame.f_code.co_filename}:{frame.f_lineno}"
    log_activity(f"{file_info} - {message}", LogSeverity.DEBUG, channel)
