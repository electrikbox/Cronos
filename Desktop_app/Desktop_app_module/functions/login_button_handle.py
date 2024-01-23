import flet as ft
from Desktop_app_module import Elements, Pages
from Desktop_app_module.functions.api_request import CronScraper
from Desktop_app_module.functions.check_command import CheckCommand


WRONG_CREDENTIALS_MSG = "Wrong username or password"
NOT_ENOUGH_ELEMENTS_MSG = "Not enough elements in cron data to check"
INFOS_TEXT_COLOR = "red"


def login(elements: Elements, page: ft.Page, pages: Pages) -> None:
    username = elements.username_field.value
    password = elements.password_field.value

    elements.login_button.disabled = True
    elements.username_field.value = ""
    elements.password_field.value = ""

    # Check if the user exist in server datas
    # =========================================================================

    try:
        cron_scraper = CronScraper(username, password)
        cron_scraper.user_auth()
    except Exception as e:
        print(e)
        elements.login_info_text.value = "server offline"
        elements.login_info_text.color = INFOS_TEXT_COLOR
        page.update()
        return

    # if not cron_scraper.authenticated:
    #     elements.login_info_text.value = WRONG_CREDENTIALS_MSG
    #     elements.login_info_text.color = INFOS_TEXT_COLOR
    #     page.update()
    #     return

    print("Authentification réussie.")

    # Check if the commands exist on computer
    # =========================================================================

    crons_list = cron_scraper.get_crons_list()

    for cron in crons_list:
        cron_split = str(cron["cron"]).split(" ")

        if len(cron_split) > 1:
            validated = CheckCommand.is_command_available_unix(cron_split[1])
            print(f"{cron['cron']} : {'added' if validated else '*NOT ADDED*'}")
        else:
            print(NOT_ENOUGH_ELEMENTS_MSG)

    # Change app page if user exist
    # =========================================================================

    page.clean()
    page.add(pages.logout_page)
    page.update()
