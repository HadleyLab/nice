from nicegui import ui
from components.ui_elements.base.builder import BaseLayout

def create():
    """Application settings page"""
    with BaseLayout() as content:
        ui.label("Settings").classes('text-3xl font-bold mb-4')
        with ui.card().classes('w-full p-4 gap-4'):
            ui.toggle(['Light', 'Dark'], value='Light').props('label="Theme"')
            ui.slider(min=0, max=100, value=75).props('label="Volume"')
