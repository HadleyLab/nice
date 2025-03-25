from components.configs.button_task_series_config import ButtonTaskSeriesConfig
from components.builders.button_task_builder import ButtonTaskBuilder
from components.utils.notifications import log_and_notify, LogSeverity
from nicegui import ui
import asyncio

class ButtonTaskSeriesBuilder:
    """Coordinates execution of multiple ButtonTasks in sequence (renamed from ButtonSeriesBuilder)"""
    
    def __init__(self, config: ButtonTaskSeriesConfig, task_builders: dict[str, ButtonTaskBuilder]):
        self.config = config
        self.task_builders = task_builders
        self._create_ui()
        
    def _create_ui(self):
        """Build series UI components"""
        self.container = ui.column()
        with self.container:
            with ui.button(self.config.button_label).props(f"color={self.config.button_color}") as self.btn:
                self.btn.on("click", self._execute_task)
            
            self.status_label = ui.label().classes("text-sm ml-2")

    def delete(self):
        """Clean up all UI components"""
        self.container.delete()

    async def _execute_task(self):
        """Coordinate execution of multiple ButtonTasks in sequence"""
        self._set_ui_state(running=True)
        task_results = []
        total_tasks = len(self.config.tasks)
        
        try:
            progress_bar = None
            if self.config.show_progress:
                with self.container:
                    progress_bar = ui.linear_progress(value=0).classes("w-full mt-2")
                    progress_bar.props("instant-feedback rounded")

            for idx, task_name in enumerate(self.config.tasks, 1):
                if task_name not in self.task_builders:
                    raise KeyError(f"Task '{task_name}' not found in registered builders")

                task = self.task_builders[task_name]
                self.status_label.set_text(f"Running: {task.config.task_name} ({idx}/{total_tasks})")
                
                try:
                    await task._execute_task()
                    task_results.append(True)
                    
                    if progress_bar:
                        progress_bar.value = idx / total_tasks
                    
                    if self.config.completion_delay > 0:
                        await asyncio.sleep(self.config.completion_delay)
                except Exception as e:
                    task_results.append(False)
                    log_and_notify(f"Task failed: {task.config.task_name} - {str(e)}",
                                  notification_type="negative",
                                  log_severity=LogSeverity.ERROR,
                                  channel="errors",
                                  duration=self.config.notification_duration)
                    if self.config.abort_on_failure:
                        raise RuntimeError("Series aborted due to task failure") from e
                            
            success = all(task_results)
            message = self.config.success_label if success else self.config.error_label
            self._show_result(success, message)
                
        except asyncio.TimeoutError:
            self._show_result(False, f"Series timed out after {self.config.timeout}s")
        except Exception as e:
            self._show_result(False, f"{self.config.error_label}: {str(e)}")
        finally:
            self._set_ui_state(running=False)
            self.status_label.set_text("")

    def _set_ui_state(self, running: bool):
        """Update UI elements based on task state"""
        self.btn.props(f"loading={'spin' if running else ''}")
        self.status_label.set_text("Running series..." if running else "")

    def _show_result(self, success: bool, message: str):
        """Display series outcome notification"""
        log_and_notify(message,
                      notification_type="positive" if success else "negative",
                      log_severity=LogSeverity.INFO,
                      channel="series",
                      duration=self.config.notification_duration)
