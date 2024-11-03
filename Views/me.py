import flet as ft
import os

class Me(ft.Page):
    def __init__(self):
        super.__init__()

    def  build(self):
        self.Navigation = ft.CupertinoNavigationBar(bgcolor=ft.colors.WHITE24, on_change=lambda _: route_change(_),
                            destinations=[
                                ft.NavigationBarDestination(icon=ft.icons.HOME_OUTLINED, label="Home"),
                                ft.NavigationBarDestination(icon=ft.icons.PERSON_OUTLINE, label="You"),
                                ft.NavigationBarDestination(icon=ft.icons.MENU, label="Menu"),
                                ]
                            )
        self.Username_Text = ft.Text(text_align=ft.TextAlign.CENTER, top=True)
        self.Avatar = ft.Stack(
                        [
                            ft.CircleAvatar(
                                content= ft.Icon(ft.icons.PERSON),
                            ),
                            ft.IconButton(
                                icon= ft.icons.PERSON,
                                on_click=lambda _: self.go('/profile')
                            )
                        ],
                        width=50,
                        height=50
                    )
        self.Profile = ft.Row(
                        [
                            self.Avatar,
                            ft.Container(
                                content=self.Username_Text,
                                on_click=lambda _:self.go('/profile')
                            ),
                        ],
                    )
        self.YourOrders = ft.ElevatedButton('Your Orders', on_click=lambda _: self.go('/yourorders'))
        self.BuyAgain = ft.ElevatedButton('Buy Again')
        self.YourAccount = ft.ElevatedButton('Your Account')
        self.Favourites = ft.ElevatedButton('Favourites')

        self.PastService_Label = ft.Text('Service History')
        self.PastServices_List = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True,horizontal=True)

        self.PastService = ft.Column(
                            [
                                self.PastService_Label,
                                self.PastServices_List
                            ]
                        )
        

        self.firstRow = ft.Row(
                        [
                            self.YourOrders,
                            self.BuyAgain
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    )
        self.secondRow = ft.Row(
                        [
                            self.YourAccount,
                            self.Favourites
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    )

        meView = ft.View(
            "/me",
                [
                    self.Profile,
                    self.firstRow,
                    self.secondRow,
                    self.PastService,
                    self.Navigation
                ]
            )
        
        self.views.append(meView)
        self.Navigation.selected_index = 1
        self.Username_Text.value = 'Hello, '+self.client_storage.get(os.getenv('USERNAME_TEXT'))
        
        self.go('/me')
        self.update(self.Username_Text)
        
        def route_change(_):
            match _.control.selected_index:
                case 0:
                    self.go('/home')
                case 1:
                    self.go('/me')
                case 2:
                    self.go('/menu')
        
        