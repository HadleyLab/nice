from dataclasses import dataclass

@dataclass
class ButtonConfig:
    task_name: str
    initial_color: str = "primary"
    active_color: str = "blue"
    success_color: str = "positive"
    error_color: str = "negative"
    initial_icon: str = "play_arrow"
    active_icon: str = "autorenew"
    success_icon: str = "check_circle"
    error_icon: str = "error"
    notification_duration: int = 3000
    log_severity: str = "info"

    def __post_init__(self):
        """Validate configuration values"""
        if not self.task_name:
            raise ValueError("Task name is required")
        if not all([self.initial_color, self.active_color, self.success_color, self.error_color]):
            raise ValueError("All color fields must be set")
        if not all([self.initial_icon, self.active_icon, self.success_icon, self.error_icon]):
            raise ValueError("All icon fields must be set")
        if self.notification_duration < 0:
            raise ValueError("Notification duration must be positive")
