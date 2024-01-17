import flet as ft
from Desktop_app_module import Elements, Pages


def login(elements: Elements, page: ft.Page, pages: Pages) -> None:
    elements.login_info_text.value = "Connected"
    elements.login_info_text.color = ft.colors.TEAL_400

    page.clean()
    page.add(pages.logout_page)
    elements.username_field.value = ""
    elements.password_field.value = ""
    page.update()
