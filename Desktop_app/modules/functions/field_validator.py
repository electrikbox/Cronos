"""Activate the login button when entering username and password in fields"""

import flet as ft
from modules import Elements


def validate(elements: Elements, page: ft.Page) -> None:
    username = elements.username_field.value
    password = elements.password_field.value
    elements.login_button.disabled = not all([username, password])
    page.update()
