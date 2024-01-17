"""class to init app pages"""

import flet as ft
from Desktop_app_module import Elements


class Pages(ft.UserControl):
    def __init__(self, elements: Elements) -> None:
        self.elements = elements

        # login page elements
        # =====================================================================

        self.login_page = ft.Column(
            [
                ft.Row(
                    [self.elements.logo],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [self.elements.username_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [self.elements.password_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [self.elements.login_info_text],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [self.elements.login_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )

        # logout page elements
        # =====================================================================

        self.logout_page = ft.Column(
            [
                ft.Row(
                    [self.elements.logo],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[ft.Text(value="Connected", color="green")],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [self.elements.logout_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [self.elements.logged_text],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )  #
