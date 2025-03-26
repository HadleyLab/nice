from nicegui import ui, app
from components.ui_elements.button.config import ButtonConfig
from components.ui_elements.series.builder import SeriesBuilder
from components.ui_elements.series.config import SeriesConfig
import pages.home  # Ensures home page registration

def register_pages():
    """Register all application pages"""
    app.add_static_files("/pages", "pages")
    
    @ui.page("/")
    def home():
        pages.home.create()
        
    @ui.page("/settings")
    def settings():
        ui.label("Settings Page").classes("text-2xl")
        # Add settings components here

if __name__ in {"__main__", "__mp_main__"}:
    register_pages()
    ui.run(title="Component Demo", port=8080)
