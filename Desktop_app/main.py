"""Desktop app main, script that launch the app"""

import flet as ft
from Desktop_app_module import Elements, AppPages, logout, validate
from Desktop_app_module.functions.login_button_handle import AppHandler


def main(page: ft.Page) -> None:
    # init app windows
    # =========================================================================

    page.title = "Cronos connect"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.START
    page.window_width = 350
    page.window_min_width = 450
    page.window_height = 400
    page.window_min_height = 500
    page.update()

    # init elements and pages
    # =========================================================================

    elements = Elements()
    elements.login_button.disabled = True
    app_pages = AppPages(elements)

    # Validate there's something in username and password fields
    # =========================================================================

    elements.username_field.on_change = lambda e: validate(elements, page)
    elements.password_field.on_change = lambda e: validate(elements, page)

    # Set functions for button click
    # =========================================================================

    app_logic = AppHandler(elements, page, app_pages)

    elements.login_button.on_click = lambda e: app_logic.login(page, app_pages)
    elements.logout_button.on_click = lambda e: logout(elements, page, app_pages)

    page.add(app_pages.login_page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

# compliation :
# export PATH=$PATH:~/.local/bin
# flet pack main.py --add-data "assets:assets"
