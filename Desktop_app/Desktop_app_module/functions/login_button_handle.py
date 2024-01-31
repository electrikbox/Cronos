import flet as ft
from Desktop_app_module import Elements, AppPages
from Desktop_app_module.functions.api_request import CronScraper
from Desktop_app_module.functions.check_command import CheckCommand
from crontab import CronTab, CronItem


WRONG_CREDENTIALS_MSG = "Wrong username or password"
NOT_ENOUGH_ELEMENTS_MSG = "Not enough elements in cron data to check"
INFOS_TEXT_COLOR = "red"


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

    def crons_lists(self) -> tuple[list[dict], CronTab]:
        remote_crons = CronScraper(self.username, self.password).get_remote_crons(self.token)
        local_crons = CronTab(user=True)
        return remote_crons, local_crons

    def update_page(self) -> None:
        self.page.clean()
        self.page.add(self.app_pages.logout_page)
        self.page.update()

    # AUTHENTICATION
    # =========================================================================

    def authenticate(self) -> None:
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

    def add_remote_crons_to_local(self) -> None:
        remote_crons, local_crons = self.crons_lists()

        for r_cron in remote_crons:

            command = str(r_cron["command"]).split(" ")[0]
            cmd_validated = CheckCommand.is_command_available_unix(command)
            r_cron_str = self.remote_cron_to_str(r_cron)

            if not cmd_validated:
                print(f"{command} : can't be process on this computer")
                continue

            # cron_scraper.send_validation(cron)

            if any(r_cron_str == self.local_cron_to_str(l_cron) for l_cron in local_crons):
                continue

            new_cron = local_crons.new(command=command, comment=self.COMMENT)
            new_cron.setall(r_cron_str.split(" ")[:5])
            local_crons.write()
            print(f"{new_cron} : added")

            # ajouter message pour l'utilisateur
            # self.update_page()

    # DEL CRON
    # =========================================================================

    def del_local_crons(self) -> None:
        remote_crons, local_crons = self.crons_lists()

        for l_cron in local_crons:
            l_cron_str = self.local_cron_to_str(l_cron)

            if l_cron.comment != self.COMMENT:
                continue

            if any(l_cron_str == self.remote_cron_to_str(r_cron) for r_cron in remote_crons):
                continue

            local_crons.remove(l_cron)
            local_crons.write()
            print(f"{l_cron_str} : removed")


    # PAUSE CRON
    # =========================================================================

    def toggle_pause_local_crons(self) -> None:
        remote_crons, local_crons = self.crons_lists()

        for r_cron in remote_crons:
            r_cron_str = self.remote_cron_to_str(r_cron)

            for l_cron in local_crons:
                l_cron_str = self.local_cron_to_str(l_cron)

                if r_cron_str != l_cron_str:
                    continue

                is_paused = r_cron["is_paused"]
                is_enabled = l_cron.is_enabled()

                if is_paused and is_enabled:
                    l_cron.enable(False)
                    print(f"{l_cron} : paused")
                elif not is_paused and not is_enabled:
                    l_cron.enable(True)
                    print(f"{l_cron} : enabled")

        local_crons.write()


            # if r_cron["is_paused"]:
            #     for l_cron in local_crons:
            #         l_cron_str = self.local_cron_to_str(l_cron)

            #         if r_cron_str == l_cron_str and l_cron.is_enabled():
            #             l_cron.enable(False)
            #             print(f"{l_cron} : paused")
            # else:
            #     for l_cron in local_crons:
            #         l_cron_str = self.local_cron_to_str(l_cron)

            #         if r_cron_str == l_cron_str and not l_cron.is_enabled():
            #             l_cron.enable(True)
            #             print(f"{l_cron} : enabled")

            # for l_cron in local_crons:
            #     l_cron_str = self.local_cron_to_str(l_cron)
            #     if r_cron["is_paused"] and r_cron_str == l_cron_str and l_cron.is_enabled():
            #         l_cron.enable(False)
            #         print(f"{l_cron} : paused")
            #     elif not r_cron["is_paused"] and r_cron_str == l_cron_str and not l_cron.is_enabled():
            #         l_cron.enable(True)
            #         print(f"{l_cron} : enabled")

    # MAIN METHODS
    # =========================================================================

    def login(self) -> None:
        self.authenticate()
        self.add_remote_crons_to_local()
        self.del_local_crons()
        self.toggle_pause_local_crons()

    def fetch_remote_crons(self) -> None:
        self.add_remote_crons_to_local()
        self.del_local_crons()
        self.toggle_pause_local_crons()
