"""Class init elements like buttons, fields"""

import flet as ft
from flet import ElevatedButton, Image, ImageFit, Text, TextField

USERNAME_FIELD_TEXT = "Username"
PASSWORD_FIELD_TEXT = "Password"
LOGIN_BTN_TEXT = "Login"
LOGOUT_BTN_TEXT = "Logout"
INFO_TEXT = "Please login"
LOGO = "logo.gif"


class Elements(ft.UserControl):
    def __init__(self) -> None:

        # Logo
        # =====================================================================

        self.logo = Image(
            src=LOGO,
            width=150,
            height=150,
            fit=ImageFit.CONTAIN
        )

        # Username field
        # =====================================================================

        self.username_field = TextField(
            label=USERNAME_FIELD_TEXT,
            text_align=ft.TextAlign.LEFT,
            width=250,
            height=45,
        )

        # Password field
        # =====================================================================

        self.password_field = TextField(
            label=PASSWORD_FIELD_TEXT,
            text_align=ft.TextAlign.LEFT,
            width=250,
            height=45,
            password=True,
        )

        # Login button
        # =====================================================================

        self.login_button = ElevatedButton(
            text=LOGIN_BTN_TEXT,
            width=200,
        )
        self.login_info_text = Text(
            INFO_TEXT,
            color=ft.colors.TEAL_400,
        )

        # MSG
        # =====================================================================

        self.cron_action_text = ft.Text(
            value="",
            color="pink"
        )

        # Fetch button
        # =====================================================================

        self.fetch_button = ElevatedButton(
            text="Refresh your crons",
            width=200,
        )
        self.fetch_info_text = Text(
            INFO_TEXT,
            color=ft.colors.TEAL_400,
        )

        # Logout button
        # =====================================================================

        self.logout_button = ElevatedButton(
            text=LOGOUT_BTN_TEXT,
            width=200
        )
        self.logged_text = Text(
            "",
            color=ft.colors.TEAL_400,
        )
