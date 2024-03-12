import flet as ft
from modules import Elements, AppPages, validate
from modules.functions.app_handler import AppHandler


def main(page: ft.Page) -> None:
    """ Main function """

    # init app windows
    # =========================================================================

    page.title = "Cronos-Connect"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.START
    page.window_width = 400
    page.window_min_width = 500
    page.window_height = 550
    page.window_min_height = 550
    page.scroll = False
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

    elements.login_button.on_click = lambda e: app_logic.login()
    elements.clear_button.on_click = lambda e: app_logic.clear_msg()
    elements.fetch_button.on_click = lambda e: app_logic.auto_fetch_on_off()
    elements.logout_button.on_click = lambda e: app_logic.logout()

    page.add(app_pages.login_page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

# compliation :
# export PATH=$PATH:~/.local/bin
# flet pack main.py --add-data "assets:assets"
