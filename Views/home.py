import flet as ft
import os
import bcrypt

class Home(ft.Page):
    def __init__(self):
        super.__init__()

    def  build(self):
        # self.suggested_item = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self.search = ft.TextField(autofocus=False, hint_text='Search', prefix_icon=ft.icons.SEARCH, 
                                    # on_change=lambda e: suggest_items(e),
                                     on_focus=lambda _: self.go('/search'), 
                                    #  on_blur=lambda e:remove_list(e)
                                )
        self.navigation = ft.CupertinoNavigationBar(
                        bgcolor=ft.colors.WHITE24,
                        on_change=lambda e: route_change(e),
                        destinations=[
                            ft.NavigationBarDestination(icon=ft.icons.HOME_OUTLINED, label="Home"),
                            ft.NavigationBarDestination(icon=ft.icons.PERSON_OUTLINE, label="You"),
                            ft.NavigationBarDestination(icon=ft.icons.MENU, label="Menu"),
                        ]
                    )
        self.items = ft.GridView(expand=1, 
                                 runs_count=5,
                                 max_extent=150,
                                 child_aspect_ratio=1.0,
                                 spacing=5,
                                 run_spacing=5)

        HomeView = ft.View(
            "/home",
                [
                    self.search,
                    # self.suggested_item,
                    self.items,
                    self.navigation
                ]
            )
        
        
        self.views.clear()
        self.views.append(HomeView)
        self.go('/home')

        def route_change(e):
            match e.control.selected_index:
                case 0:
                    self.go('/home')
                case 1:
                    self.go('/me')
                case 2:
                    self.go('/menu')
        # return HomeView