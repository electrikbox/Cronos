import flet as ft
from Desktop_app_module import Elements, Pages
from Desktop_app_module.functions.api_request import CronScraper
from Desktop_app_module.functions.check_command import CheckCommand
from Desktop_app_module.functions.cron_handler import CronHandler


WRONG_CREDENTIALS_MSG = "Wrong username or password"
NOT_ENOUGH_ELEMENTS_MSG = "Not enough elements in cron data to check"
INFOS_TEXT_COLOR = "red"


def login(elements: Elements, page: ft.Page, pages: Pages) -> None:
    username = elements.username_field.value
    password = elements.password_field.value

    elements.login_button.disabled = True
    elements.username_field.value = ""
    elements.password_field.value = ""

    # Check if the user exists in server datas
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

    if not cron_scraper.authenticated:
        elements.login_info_text.value = WRONG_CREDENTIALS_MSG
        elements.login_info_text.color = INFOS_TEXT_COLOR
        page.update()
        return

    print("Successful authentication")

    # Crons lists settings
    # =========================================================================

    remote_crons = cron_scraper.get_crons_list()
    local_crons = CronHandler.get_local_crons()
    cron_handler = CronHandler()

    # Delete if cron is not in DB
    # =========================================================================

    remote_list = []

    for r_cron in remote_crons:
        schedule, cmd = cron_handler.remote_cron_json_to_str(r_cron)
        remote_list.append(f"{schedule} {cmd} # {cron_handler.COMMENT}")

    for cron in local_crons:
        if str(cron) not in remote_list:
            cron_handler.del_cron(cron)

    # Add crons if commands is executable on computer
    # =========================================================================

    # add if cmd is executable on computer
    for cron in remote_crons:
        command = str(cron["command"]).split(" ")[0]
        cmd_validated = CheckCommand.is_command_available_unix(command)
        # cron_scraper.send_validation(cron)

        if not cmd_validated:
            print(f"{command} : *NOT ADDED*")
        else:
            if cron['is_paused']:
                cron_handler.pause_cron(cron)
            cron_handler.add_cron(cron)

    # Change app page if user exist
    # =========================================================================

    page.clean()
    page.add(pages.logout_page)
    page.update()
