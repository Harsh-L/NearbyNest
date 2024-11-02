import flet as ft

class Search(ft.Page):
    def __init__(self):
        super.__init__()

    def  build(self):
        self.suggested_item = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True, width=self.search.width)
        self.search = ft.TextField(autofocus=True,hint_text='Search', prefix_icon=ft.icons.SEARCH, 
                                    on_change=lambda e: suggest_items(e),
                                    expand=True)
        self.searchRef = ft.Text(text_align=ft.TextAlign.LEFT)
        self.back_button = ft.TextButton(
                            content=ft.Icon(name=ft.icons.ARROW_BACK),
                            on_click=lambda _:self.go('/home'),
                            style=ft.ButtonStyle(
                                shape={
                                    '': ft.RoundedRectangleBorder()
                                }
                            )
                        )
        self.clear_button = ft.TextButton(
                            content=ft.Icon(name=ft.icons.CLOSE),
                            visible=False,
                            on_click=lambda _: clearSearch(_),
                            style=ft.ButtonStyle(
                                shape={
                                    '': ft.RoundedRectangleBorder()
                                }
                            )
                        )


        SearchView = ft.View(
            "/search",
                [
                            ft.Row(
                                controls=[
                                    self.back_button,
                                    self.search,
                                    self.clear_button
                                ]
                            ),
                            # self.back_button,
                            # self.search,
                            # self.clear_button


                    self.suggested_item,
                ]
            )
        
        self.views.clear()
        self.views.append(SearchView)
        self.go('/search')

        def clearSearch(e):
            self.search.value = ''
            self.clear_button.visible = False
            remove_list(e)
            self.update()

        def remove_list(e):
            self.suggested_item.visible = False
            self.suggested_item.controls.clear()
            self.update()

        def suggest_items(e):
            self.suggested_item.visible = True
            self.suggested_item.controls.clear()
            # self.suggested_item.controls.append(ft.TextButton('Test', on_click=lambda e:print(e)))
            if e.control.value != '':
                self.clear_button.visible = True
                self.searchRef.value = e.control.value
                self.suggested_item.controls.append(ft.TextButton(
                                                        # expand=True,
                                                        content=ft.Row(
                                                                    alignment=ft.MainAxisAlignment.START,
                                                                    controls=[
                                                                        ft.Icon(ft.icons.SEARCH),
                                                                        ft.Text(value=self.searchRef.value)
                                                                    ],
                                                                    data=self.searchRef.value
                                                                ),
                                                        on_click=lambda _: openItem(_),
                                                        style=  ft.ButtonStyle(
                                                                shape={
                                                                    '': ft.RoundedRectangleBorder()
                                                                }
                                                            )
                                                        )
                                                    )
                # self.suggested_item.controls.append(ft.ListTile(
                #                                         title='self.searchRef.value',
                #                                         leading=ft.Icon(ft.icons.SEARCH),
                #                                         trailing=ft.Icon(ft.icons.ARROW_OUTWARD)
                #                                     ))
            else:
                self.clear_button.visible = False
                self.suggested_item.controls.clear()
            self.update()

        def route_change(e):
            match e.control.selected_index:
                case 0:
                    self.go('/home')
                case 1:
                    self.go('/me')
                case 2:
                    self.go('/menu')
        
        def openItem(_):
            self.go('/item', q=self.searchRef.value)
        # return SearchView