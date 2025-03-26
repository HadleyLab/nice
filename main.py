from nicegui import ui
from components.ui_elements.base.builder import BaseLayout
from pages.home import create as create_home
from pages.about import create as create_about
from pages.settings import create as create_settings

@ui.page('/')
def home_page():
    """Home page route"""
    with BaseLayout() as content:
        create_home()

@ui.page('/about')
def about_page():
    """About page route"""
    with BaseLayout() as content:
        create_about()

@ui.page('/settings')
def settings_page():
    """Settings page route"""
    with BaseLayout() as content:
        create_settings()

# Theme configuration
ui.run(
    title='My NiceGUI App',
    reload=False,
    dark=False,
    favicon='https://nicegui.io/favicon.ico',
    port=8081
)
