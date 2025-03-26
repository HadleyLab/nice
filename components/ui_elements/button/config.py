from ..base.config import BaseConfig, SeverityLevel

class ButtonConfig(BaseConfig):
    """Configuration for interactive button elements"""
    task_name: str = "New Task"
    default_icon: str = "play_arrow"
    active_icon: str = "hourglass_empty" 
    completion_icon: str = "check"
    notification_duration: int = 3000
    failure_rate: float = 0.2  # 20% simulated failure chance
    severity: SeverityLevel = SeverityLevel.INFO

    def __init__(self,
                 uid: str,
                 task_name: str = "New Task",
                 severity: SeverityLevel = SeverityLevel.INFO,
                 **kwargs):
        super().__init__(uid=uid)
        self.task_name = task_name
        self.color = severity.value
        self.__dict__.update(kwargs)

    def validate(self):
        super().validate()
        if not self.task_name:
            raise ValueError("Task name is required")
        if not 0 <= self.failure_rate <= 1:
            raise ValueError("Failure rate must be between 0 and 1")
