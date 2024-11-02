import flet as ft
from Controller.controller import controller
import dotenv, os, bcrypt

def main(page: ft.Page):
    dotenv.load_dotenv()
    if page.client_storage.contains_key(os.getenv('APP_THEME')):
        match page.client_storage.get(os.getenv('APP_THEME')):
            case 'ThemeMode.LIGHT':
                page.theme_mode = ft.ThemeMode.LIGHT
            case 'ThemeMode.DARK':
                page.theme_mode = ft.ThemeMode.DARK
            case _:
                page.theme_mode = ft.ThemeMode.SYSTEM
    else:
        page.theme_mode = ft.ThemeMode.SYSTEM
    page.update()

    page.theme = ft.Theme(color_scheme_seed='#769CDF',
                          visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY, 
                          )

    def route_change(route):
        controller(page)

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go('/')

ft.app(target=main)