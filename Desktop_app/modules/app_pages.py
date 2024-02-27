"""class to init app pages"""

import flet as ft
from modules import Elements


class AppPages(ft.UserControl):
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
                    [self.elements.cron_action_text],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Row(
                            controls=[
                                ft.Text(value="Connected", color="green")],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(
                            content=self.elements.fetch_button,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=self.elements.clear_button,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=self.elements.logout_button,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=self.elements.logged_text,
                            alignment=ft.alignment.center,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )
