import flet as ft
from Desktop_app_module import Elements, AppPages
from Desktop_app_module.functions.api_request import CronScraper
from Desktop_app_module.functions.check_command import CheckCommand
from crontab import CronTab, CronItem


WRONG_CREDENTIALS_MSG = "Wrong username or password"
NOT_ENOUGH_ELEMENTS_MSG = "Not enough elements in cron data to check"
INFOS_TEXT_COLOR = "red"



    # Delete if cron is not in DB
    # =========================================================================

    # remote_list = []

    # for r_cron in remote_crons:
    #     schedule, cmd = cron_handler.remote_cron_json_to_str(r_cron)
    #     remote_list.append(f"{schedule} {cmd} # {cron_handler.COMMENT}")

    # for cron in local_crons:
    #     if str(cron) not in remote_list:
    #         cron_handler.del_cron(cron)



class AppHandler():
    COMMENT = "Cronos"

    def __init__(self, elements: Elements, page: ft.Page, app_pages: AppPages) -> None:
        self.elements = elements
        self.page = page
        self.app_pages = app_pages

        self.username = ""
        self.password = ""
        self.token = None

    # UTILS
    # =========================================================================

    def remote_cron_to_str(self, cron: dict) -> str:
        cmd = cron['command']
        schedule = " ".join([
            cron['minutes'],
            cron['hours'],
            cron['day_of_month'],
            cron['months'],
            cron['day_of_week'],
        ])
        remote_cron_str = f"{schedule} {cmd} # {self.COMMENT}"
        return remote_cron_str

    def local_cron_to_str(self, cron: CronItem) -> str:
        cmd = cron.command
        schedule = " ".join([
            str(cron.minute),
            str(cron.hour),
            str(cron.dom),
            str(cron.month),
            str(cron.dow),
        ])
        local_cron_str = f"{schedule} {cmd} # {cron.comment}"
        return local_cron_str

    def update_page(self):
        self.page.clean()
        self.page.add(self.app_pages.logout_page)
        self.page.update()

    # AUTHENTICATION
    # =========================================================================

    def authenticate(self):
        self.username = self.elements.username_field.value
        self.password = self.elements.password_field.value

        self.elements.login_button.disabled = True
        self.elements.username_field.value = ""
        self.elements.password_field.value = ""

        try:
            cron_scraper = CronScraper(self.username, self.password)
            self.token = cron_scraper.user_auth()
        except Exception as e:
            print(e)
            self.elements.login_info_text.value = "server offline"
            self.elements.login_info_text.color = INFOS_TEXT_COLOR
            self.page.update()
            return

        if not cron_scraper.authenticated:
            self.elements.login_info_text.value = WRONG_CREDENTIALS_MSG
            self.elements.login_info_text.color = INFOS_TEXT_COLOR
            self.page.update()
            return

        print("Successful authentication")
        self.update_page()

    # ADD CRON
    # =========================================================================

    def add_remote_crons_to_local(self):
        remote_crons = CronScraper(self.username, self.password).get_remote_crons(self.token)
        local_crons = CronTab(user=True)

        for r_cron in remote_crons:

            command = str(r_cron["command"]).split(" ")[0]
            cmd_validated = CheckCommand.is_command_available_unix(command)
            r_cron_str = self.remote_cron_to_str(r_cron)
            print(f"{r_cron_str} : {cmd_validated}")

            if not cmd_validated:
                print(f"{command} : can't be process on this computer")
                continue

            if any(r_cron_str == self.local_cron_to_str(l_cron) for l_cron in local_crons):
                print(f"Cron ({r_cron_str}) already exist")
                continue

            new_cron = local_crons.new(command=command, comment=self.COMMENT)
            new_cron.setall(r_cron_str.split(" ")[:5])
            local_crons.write()
            print(f"Cron '{new_cron}' added")

            # cron_scraper.send_validation(cron)
            # ajouter message pour l'utilisateur
            # self.update_page()

    # DEL CRON
    # =========================================================================

    # PAUSE CRON
    # =========================================================================



    # MAIN METHODS
    # =========================================================================

    def login(self, page: ft.Page, app_pages: AppPages) -> None:
        self.authenticate()
        self.add_remote_crons_to_local()


    def fetch_remote_crons(self, page: ft.Page, app_pages: AppPages) -> None:
        self.add_remote_crons_to_local()
