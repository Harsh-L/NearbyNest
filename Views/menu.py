import flet as ft
import os

class Menu(ft.Page):
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
        self.isServiceProvider_label = ft.Text(value='Work as Service Provider')
        self.isServiceProvider = ft.Switch(label_position=ft.LabelPosition.LEFT, 
                                  adaptive=True,
                                  value=False, 
                                  splash_radius=10,
                                  )
        
        self.AppTheme_label = ft.Text(value='Dark Mode')
        self.AppTheme = ft.Switch(label_position=ft.LabelPosition.LEFT, 
                                  adaptive=True,
                                  value=False, 
                                  splash_radius=10,
                                  on_change=lambda _: ChangeTheme(_))
        self.ServiceHistory = ft.ElevatedButton('Service History', on_click=lambda _: self.go('/servicehistory'))
        self.BuyAgain = ft.ElevatedButton('Buy Again')
        self.YourAccount = ft.ElevatedButton('Your Account')
        self.Favourites = ft.ElevatedButton('Favourites')
        self.signOut = ft.ElevatedButton(text='Sign Out',expand=True, 
                                         style=ft.ButtonStyle(
                                             shape={
                                                 '':ft.RoundedRectangleBorder(radius=10)
                                                }
                                            ),
                                            on_click=lambda _: LogOut(_)
                                    )

        self.firstRow = ft.Row(
                        [
                            self.ServiceHistory,
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
            "/menu",
                [
                    ft.Row(controls=[self.isServiceProvider_label, self.isServiceProvider],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row(controls=[self.AppTheme_label, self.AppTheme],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    self.firstRow,
                    self.secondRow,
                    self.Navigation,
                    ft.Row(controls=[self.signOut]),
                    
                ]
            )
        
        self.views.append(meView)

        self.Navigation.selected_index = 2
        if self.theme_mode == ft.ThemeMode.LIGHT:
            self.AppTheme.value = False
        if self.theme_mode == ft.ThemeMode.DARK:
            self.AppTheme.value = True
        
        self.go('/menu')
        
        def LogOut(e):
            if self.client_storage.contains_key(os.getenv('USERNAME_TEXT')):
                self.client_storage.remove(os.getenv('USERNAME_TEXT'))
            if self.client_storage.contains_key(os.getenv('PASSWORD_TEXT')):
                self.client_storage.remove(os.getenv('PASSWORD_TEXT'))
            self.views.clear()
            self.go('/')

        def ChangeTheme(_):
            if self.AppTheme.value == True:
                self.theme_mode = ft.ThemeMode.DARK
            else:
                self.theme_mode = ft.ThemeMode.LIGHT

            self.client_storage.set(os.getenv('APP_THEME'), str(self.theme_mode))
            self.update()

        def route_change(_):
            match _.control.selected_index:
                case 0:
                    self.go('/home')
                case 1:
                    self.go('/me')
                case 2:
                    self.go('/menu')
        
        