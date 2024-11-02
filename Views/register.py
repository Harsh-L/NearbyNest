import flet as ft
import bcrypt, re, dotenv, os
from flet.auth.providers import GoogleOAuthProvider
import random
from Model.send_email_otp import Email_OTP
import pyotp

class Register(ft.Page):
    def __init__(self):
        super.__init__()
        
    def  build(self):
        self.Username = ft.TextField(label='Username',autofocus=True, 
                                     on_focus=lambda _: removeStyle(self.Username))
        
        self.Password = ft.TextField(label='Password',autofocus=True,password=True, can_reveal_password=True, 
                                     on_focus=lambda _: removeStyle(self.Password), on_change=lambda _: ValidatePassword(self.Password))
        self.ReEnterPassword = ft.TextField(label='Re-Enter Password',autofocus=True,password=True, can_reveal_password=True, 
                                            on_change=lambda _: ComparePasswords(self.ReEnterPassword), 
                                            on_focus=lambda _: ComparePasswords(self.ReEnterPassword),
                                            keyboard_type=ft.KeyboardType.EMAIL)
        
        self.Address = ft.TextField(label="Address", multiline=True, min_lines=2, keyboard_type=ft.KeyboardType.STREET_ADDRESS)

        self.PhoneNo = ft.TextField(label="Phone No.", input_filter=ft.NumbersOnlyInputFilter(), keyboard_type=ft.KeyboardType.PHONE)

        self.Email = ft.TextField(label="E-mail", on_blur=lambda _: ValidateEmail(self.Email), keyboard_type=ft.KeyboardType.EMAIL)

        self.incorrectCredentials_Alert = ft.AlertDialog(title=ft.Text('Incorrect Username or Password'), on_dismiss=lambda _: clearPassword(self.Password))
        self.emptyCredentialsAlert = ft.AlertDialog(title=ft.Text('Username or Password can\'t be empty'), on_dismiss=lambda _: clearPassword(self.Password))
        self.emptyEmailAlter = ft.AlertDialog(title=ft.Text('E-mail can\'t be empty'))
        self.signupText = ft.Text('New to farm2U?')
        self.signupLink = ft.TextButton('Sign up now')
        self.ErrorGeneratingOTP = ft.AlertDialog(title=ft.Text('Error generating OTP, Please try again'))
        
        # self.SignInButton = ft.ElevatedButton('Sign In', 
        #                                           style= ft.ButtonStyle(
        #                                                 shape=ft.RoundedRectangleBorder(radius=5),
        #                                             ),
        #                                           on_click=lambda e: attempt_signin(e)),
        
        PasswordValidationError: str = 'The password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@, $, !, %, #, ?, &).'
        PasswordUnmatchedError: str = 'The passwords don''t match.'
        EmailValidationError: str = 'Please enter a valid email address.'

        RegisterView = ft.View(
            "/register",
                [
                    ft.Column(
                        wrap=True,
                        alignment=ft.alignment.top_center,
                        controls=[
                            ft.Container(
                                content=ft.Text('Sign Up',text_align=ft.TextAlign.CENTER, size=30),
                            ),
                            ft.Container(
                                content=self.Username,
                            ),
                            ft.Container(
                                content=self.Password,
                            ),
                            ft.Container(
                                content=self.ReEnterPassword,
                            ),
                            ft.Container(
                                content=self.Email,
                            ),
                            ft.Container(
                                content=self.PhoneNo,
                            ),
                            ft.Container(
                                content=self.Address,
                            ),
                            ft.Container(
                                content=ft.Column(
                                            controls=[ft.ElevatedButton('Sign Up', 
                                                        style= ft.ButtonStyle(
                                                            shape=ft.RoundedRectangleBorder(radius=5),
                                                            ),
                                                        width=300,
                                                        on_click=lambda e: register(e), data='self.Username.data')],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.BASELINE
                                        ),
                            ),
                        ],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        
        self.views.append(RegisterView)
        # self.go('/register')

        def register(_):
            if (self.Username.value != '') and (self.Password.value != ''):
                ########## TODO (Email verification) ##########
                if self.Email.value != '':
                    # _OTP = random.randint(1000,9999)
                    Secret = pyotp.random_base32()
                    _OTP = pyotp.TOTP(Secret, digits=4, interval=int(os.getenv('OTP_TIMER'))).now()
                    Email_OTP.sendOTPViaEmail(self.Email.value, _OTP)
                    hashedPassword = bcrypt.hashpw(bytes(self.Password.value,'utf-8'), bcrypt.gensalt(12))
                    self.session.set(os.getenv('USERNAME_TEXT'), self.Username.value)
                    self.session.set(os.getenv('PASSWORD_TEXT'), hashedPassword.decode('utf-8'))
                    self.session.set('Email', self.Email.value)
                    self.session.set('Phone No', self.PhoneNo.value)
                    self.session.set('Address', self.Address.value)
                    self.session.set('Secret', Secret)
                    if Secret != None:
                        self.go('/emailverification')
                    else:
                        self.open(self.ErrorGeneratingOTP)
                else:
                    self.open(self.emptyEmailAlter)
                    # self.go('/home')

            else:
                self.open(self.emptyCredentialsAlert)
                # exit()
            
        def ValidateEmail(_):
            emailValidationPattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.fullmatch(emailValidationPattern, _.value) or (_.value == ''):
                self.Email.error_text = ''
            else:
                self.Email.error_text = EmailValidationError
            
            self.update()

        def ComparePasswords(_):
            if self.ReEnterPassword.value != '':
                if self.Password.value != self.ReEnterPassword.value:
                    _.error_text = PasswordUnmatchedError
                else:
                    _.error_text = ''
            else:
                _.error_text = ''
            
            self.update()

        def ValidatePassword(_):
            passwordValidationPattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
            if re.fullmatch(passwordValidationPattern, _.value) or (_.value == ''):
                _.error_text = ''
            else:
                _.error_text = PasswordValidationError
            
            self.update()


        def clearPassword(_):
            _.value = ''
            _.border_color = ft.colors.RED
            self.update()

        def removeStyle(_):
            _.border_color = None
            self.update()
        # return HomeView
        
        