import flet as ft
from modules import Elements


class AppPages(ft.UserControl):
    """ Class to initialize the pages of the app """

    def __init__(self, elements: Elements) -> None:
        """ Initialize the pages """
        self.elements = elements

        # Login page elements
        # =====================================================================

        self.login_page = ft.Column(
            [
                ft.Row(
                    [self.elements.logo],
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=180,
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
                ft.Container(
                    content=ft.Column(
                        [self.elements.copyright],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    alignment=ft.alignment.center,
                    width=350,
                    height=50,
                    expand=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        # Logout page elements
        # =====================================================================

        self.logout_page = ft.Column(
            [
                ft.Row(
                    [self.elements.logo],
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=180,
                ),
                ft.Container(
                    content=ft.Column(
                        [self.elements.cron_action_text],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=True,
                        auto_scroll=True,
                        height=120,
                        width=350,
                    ),
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, ft.colors.GREY_800),
                    border_radius=10,
                    padding=10,
                    width=350,
                ),
                ft.Column(
                    [
                        ft.Row(
                            controls=[
                                ft.Text(value="Auto fetch : ", color="white"),
                                self.elements.autofetch_txt,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    self.elements.fetch_button,
                                    self.elements.clear_button,
                                    self.elements.logout_button,
                                ],
                            ),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [self.elements.logged_text],
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=ft.Column(
                        [self.elements.copyright],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    alignment=ft.alignment.center,
                    width=350,
                    height=50,
                    expand=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
