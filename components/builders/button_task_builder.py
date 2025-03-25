from components.configs.button_task_config import ButtonTaskConfig
from components.utils.notifications import log_and_notify, LogSeverity, task_log_and_notify
from nicegui import ui, app
import asyncio

class ButtonTaskBuilder:
    """Constructs and manages an async task with UI controls"""
    
    def __init__(self, config: ButtonTaskConfig, task_id: str):
        self.config = config
        self.task_id = task_id
        self._create_ui()
        self._load_state()
        self._update_state("initial", self.config.initial_color)

    def _load_state(self):
        """Initialize from persisted state"""
        if self.task_id in app.state.tasks:
            state = app.state.tasks[self.task_id]
            self.btn.props(f"color={state['color']}")
            self.btn.set_text(state["label"])

    def delete(self):
        """Clean up all UI components"""
        self.container.delete()

    def _update_state(self, status: str, color: str):
        """Update button state with icon visibility"""
        icon_map = {
            "initial": self.config.initial_icon,
            "running": self.config.active_icon,
            "success": self.config.success_icon,
            "failed": self.config.error_icon
        }
        self.status_icon.set_name(icon_map[status])
        self.btn.props(f"color={color}")

    def _create_ui(self):
        """Build the UI components for this task"""
        self.container = ui.column().classes("w-full min-w-[300px] gap-1")
        with self.container:
            with ui.button().props(f"color={self.config.initial_color}") as self.btn:
                self.btn.on("click", self._execute_task)
                with ui.row().classes("items-center gap-2"):
                    ui.label(self.config.task_name).classes("truncate")
                    self.status_icon = ui.icon(self.config.initial_icon).classes("text-white")

    async def _execute_task(self):
        """Execute task with visual feedback"""
        try:
            self.btn.props("loading=true")
            self._update_state("running", self.config.active_color)
            self.status_icon.classes(add="animate-spin")
            await asyncio.sleep(0.8)  # Simulated work duration
            
            if hash(self.task_id) % 5 == 0:  # 20% failure rate
                raise RuntimeError("Simulated task failure")
                
            self._update_state("success", self.config.success_color)
            log_and_notify(f"{self.config.task_name} completed",
                          notification_type="positive",
                          log_severity=LogSeverity.INFO,
                          channel="tasks",
                          duration=self.config.notification_duration)
            
        except Exception as e:
            self._update_state("failed", self.config.error_color)
            task_log_and_notify(self.config.task_name, success=False, error_msg=str(e))
        finally:
            self.btn.props("loading=false")
            self.status_icon.classes(remove="animate-spin")
