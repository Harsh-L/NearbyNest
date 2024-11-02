import flet as ft
class NotFound(ft.Page):
    def __init__(self):
        super.__init__()

    def  build(self):
        NotFound = ft.View(
            "/NotFound",
                    [
                        ft.Text('404 Page Not Found', None ,ft.alignment.top_center,None,30,30,True,ft.TextStyle.letter_spacing,None,None,None,True,True,ft.colors.AMBER_ACCENT_200,ft.colors.BLUE_500)
                    ]
                )
        self.views.append(NotFound)
        self.go(self.route)