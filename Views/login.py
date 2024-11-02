import flet as ft
import bcrypt, re, dotenv, os

class Login(ft.Page):
    def __init__(self):
        super.__init__()
        
    def  build(self):
        self.Username = ft.TextField(label='Username',autofocus=True, 
                                     on_focus=lambda _: removeStyle(self.Username))
        
        self.Password = ft.TextField(label='Password',autofocus=True,password=True, can_reveal_password=True, 
                                     on_focus=lambda _: removeStyle(self.Password), on_change=lambda _: ValidatePassword(self.Password))
        
        self.incorrectCredentials_Alert = ft.AlertDialog(title=ft.Text('Incorrect Username or Password'), on_dismiss=lambda _: clearPassword(self.Password))
        self.emptyCredentialsAlert = ft.AlertDialog(title=ft.Text('Username or Password can\'t be empty'), on_dismiss=lambda _: clearPassword(self.Password))
        
        self.signupText = ft.Text('New to farm2U?')
        self.signupLink = ft.TextButton('Sign up now', on_click=lambda _:goToResisterPage(_))
        
        
        self.SignInButton = ft.ElevatedButton('Sign In', autofocus=False,
                                                style= ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=5),
                                                ),
                                              on_click=lambda e: attempt_signin(e))
        
        ValidationError: str = 'The password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@, $, !, %, #, ?, &).'


        LoginView = ft.View(
            "/",
                [
                    ft.Container(
                        content=ft.Text('Sign In',text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.top_center
                    ),
                    ft.Container(
                        content=self.Username,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=self.Password,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=self.SignInButton,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        ft.TextButton(
                            text='Forgot Password ?'
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                    content=ft.Column(
                        [
                            self.signupText,
                            self.signupLink
                        ],
                        spacing=5
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(25)
                    )
                ]
                # horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        
        self.views.clear()
        
        if self.client_storage.contains_key(os.getenv('USERNAME_TEXT')):
            loginUsername = self.client_storage.get(os.getenv('USERNAME_TEXT'))
        else:
            loginUsername = None
        if self.client_storage.contains_key(os.getenv('PASSWORD_TEXT')):
            loginPassword = self.client_storage.get(os.getenv('PASSWORD_TEXT'))
        else:
            loginPassword = None
        
        if (loginUsername != None and loginPassword != None):
            if (bcrypt.checkpw(bytes(loginUsername,'utf-8'), bytes(loginPassword, 'utf-8'))):
                self.go('/home')
            else:
                self.views.append(LoginView)
                self.go('/')
        else:
                self.views.append(LoginView)
                self.go('/')

        def attempt_signin(e):
            if (self.Username.value != '') and (self.Password.value != ''):
                hashedPassword = bcrypt.hashpw(bytes(self.Password.value,'utf-8'), bcrypt.gensalt(12))
            
                if bcrypt.checkpw(bytes(self.Username.value,'utf-8'), hashedPassword) == True:
                    self.client_storage.set(os.getenv('USERNAME_TEXT'), self.Username.value)
                    self.client_storage.set(os.getenv('PASSWORD_TEXT'), hashedPassword.decode('utf-8'))
                    self.go('/home')
                else:
                    self.open(self.incorrectCredentials_Alert)
            else:
                self.open(self.emptyCredentialsAlert)

        def ValidatePassword(_):
            passwordValidationPattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
            if re.fullmatch(passwordValidationPattern, _.value) or (_.value == ''):
                self.Password.error_text = ''
            else:
                self.Password.error_text = ValidationError
            
            self.update()

        def clearPassword(_):
            _.value = ''
            _.border_color = ft.colors.RED
            self.update()

        def removeStyle(_):
            _.border_color = None
            self.update()


        def goToResisterPage(_):
            self.views.clear()
            self.go('/register')