import urllib.parse
import flet as ft
import os
import bcrypt
import urllib
from Views.login import Login
from Views.register import Register
from Views.notfound import NotFound
from Views.home import Home
from Views.search import Search
from Views.me import Me
from Views.menu import Menu

def controller(page: ft.Page):
    # if page.route.split("?").__len__() > 1:
    #     print(page.route.split("?")[1])
    #     print(urllib.parse.urlencode(page.route.split("?")[1]))

    page.route = page.route.split("?")[0]
    match page.route:
        case '/':
            Login.build(page),
        case '/register': 
            Register.build(page)
        case '/home':
            # LoginFromClientStorage(page)
            Home.build(page),
        case '/search':
            # LoginFromClientStorage(page)
            Search.build(page),
        case '/me':
            LoginFromClientStorage(page)
            Me.build(page),
        case '/menu': 
            # LoginFromClientStorage(page)
            Menu.build(page)
        case _: NotFound.build(page)

def LoginFromClientStorage(page: ft.Page):
    username = page.client_storage.get(os.getenv('USERNAME_TEXT'))
    hashedPassword = page.client_storage.get(os.getenv('PASSWORD_TEXT'))

    if not ( ((username != None) and (hashedPassword != None)) and (bcrypt.checkpw(bytes(username, 'utf-8'), bytes(hashedPassword, 'utf-8')) == True) ):
        page.go('/')