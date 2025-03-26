from ..base.builder import BaseBuilder
from .config import ButtonConfig
from nicegui import ui

class ButtonBuilder(BaseBuilder):
    """Concrete builder implementation for button elements"""
    def __init__(self, config: ButtonConfig):
        super().__init__(config)
        self.config: ButtonConfig = config
        
    def build(self) -> ui.row:
        """Construct a button using native NiceGUI reactivity"""
        with ui.row() as container:
            self.btn = (ui.button(self.config.label)
                .props(f'icon={self.config.icon}')
                .classes(f'text-{self.config.color}')
                .bind_visibility_from(self.config, 'state', lambda s: s == 'default'))
        return container


class ButtonTaskBuilder(ButtonBuilder):
    """Task-oriented button builder extending base functionality"""
    def __init__(self, task_id: str, defaults: dict):
        config = ButtonConfig(
            task_id=task_id,
            default_icon=defaults.get('default_icon', 'play_circle'),
            active_icon=defaults.get('active_icon', 'hourglass_empty'),
            completion_icon=defaults.get('completion_icon', 'check_circle'),
            severity=defaults.get('severity', 'primary'),
            notification_duration=defaults.get('notification_duration', 2.5)
        )
        super().__init__(config)

    def build(self) -> ui.row:
        """Extend base build with task-specific handlers"""
        container = super().build()
        self.btn.on('click', lambda _: self._handle_button_click(self.config.task_id))
        return container
