import flet as ft
import os
import bcrypt

class ServiceList(ft.Page):
    def __init__(self):
        super.__init__()

    def  build(self):

        self.search = ft.TextField(autofocus=False, hint_text='Search item', prefix_icon=ft.icons.SEARCH, 
                                     on_focus=lambda _: self.go('/search'),
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
        self.items = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        ServiceListView = ft.View(
            "/servicelist",
                [
                    self.search,
                    self.items,
                    self.navigation
                ]
            )
        

        self.views.append(ServiceListView)
        if self.query.to_dict.get('q'):
            self.search.value = self.query.to_dict.get('q')
            self.go('/servicelist',q=self.query.to_dict.get('q'))
        else:
            self.go('/servicelist')
            

        #     print(self.query.to_dict.get('q'))
        #     self.search.value = self.query.to_dict.get('q')

        def route_change(e):
            match e.control.selected_index:
                case 0:
                    self.go('/home')
                case 1:
                    self.go('/me')
                case 2:
                    self.go('/menu')