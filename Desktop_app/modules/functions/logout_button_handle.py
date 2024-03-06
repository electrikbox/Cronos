import flet as ft
from modules import Elements, AppPages


def logout(elements: Elements, page: ft.Page, pages: AppPages) -> None:
    """ Logout function call """
    elements.login_info_text.value = "Please login"
    elements.login_info_text.color = ft.colors.TEAL_400
    elements.login_button.disabled = True
    page.clean()
    page.add(pages.login_page)
    page.update()
