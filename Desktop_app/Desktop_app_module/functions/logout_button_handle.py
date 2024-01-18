"""Logout function call when hiting logout button"""

import flet as ft
from Desktop_app_module import Elements, Pages


def logout(elements: Elements, page: ft.Page, pages: Pages) -> None:
    elements.login_info_text.value = "Please login"
    elements.login_info_text.color = ft.colors.TEAL_400
    elements.login_button.disabled = True
    page.clean()
    page.add(pages.login_page)
    page.update()
