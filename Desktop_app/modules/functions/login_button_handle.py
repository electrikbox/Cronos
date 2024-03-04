import flet as ft
import os
import time
from modules import Elements, AppPages
from modules.functions.api_request import CronScraper
from modules.functions.check_command import CheckCommand
from modules.functions.cron_script_handle import CronosScript
from crontab import CronTab, CronItem


WRONG_CREDENTIALS_MSG = "Wrong username or password"
NOT_ENOUGH_ELEMENTS_MSG = "Not enough elements in cron data to check"
INFOS_TEXT_COLOR = "red"


class AppHandler:
    COMMENT = "Cronos"

    def __init__(self, elements: Elements, page: ft.Page, app_pages: AppPages) -> None:
        self.elements = elements
        self.page = page
        self.app_pages = app_pages

        self.username = ""
        self.password = ""
        self.token = None

        self.cron_script_path = ""

        self.cron_action_text = self.elements.cron_action_text
        self.all_msg_in_app = []
        self.unvalid_found = False
        self.auto_fetch = True

    # UTILS
    # =========================================================================

    def remote_cron_to_str(self, cron: dict) -> str:
        """ Convert remote cron to string """
        cmd = cron["command"]
        schedule = " ".join(
            [
                cron["minutes"],
                cron["hours"],
                cron["day_of_month"],
                cron["months"],
                cron["day_of_week"],
            ]
        )
        remote_cron_str = f"{schedule} {cmd} # {self.COMMENT}"
        return remote_cron_str

    def local_cron_to_str(self, cron: CronItem) -> str:
        """ Convert local cron to string """
        cmd = cron.command
        schedule = " ".join(
            [
                str(cron.minute),
                str(cron.hour),
                str(cron.dom),
                str(cron.month),
                str(cron.dow),
            ]
        )
        local_cron_str = f"{schedule} {cmd} # {cron.comment}"
        return local_cron_str

    def crons_lists(self) -> tuple[list[dict], CronTab]:
        """ Get remote and local crons """
        remote_crons = CronScraper(
            self.username,
            self.password
        ).get_remote_crons(self.token)
        local_crons = CronTab(user=True)
        return remote_crons, local_crons

    def update_page(self) -> None:
        """ Update the page """
        self.page.clean()
        self.page.add(self.app_pages.logout_page)
        self.page.update()

    # AUTHENTICATION
    # =========================================================================

    def authenticate(self) -> None:
        """ Authenticate user """
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
        """ Add remote crons to local crontab """
        remote_crons, local_crons = self.crons_lists()

        for r_cron in remote_crons:
            id = r_cron["id"]
            cmd = r_cron["command"]

            # check if cron already exists
            if any(
                id == int(cron.comment.split("-")[1])
                for cron in local_crons
                if cron.comment and self.COMMENT in cron.comment
            ):
                continue

            # check if command is available
            command = str(cmd).split(" ")[0]
            cmd_validated = CheckCommand.is_command_available_unix(command)

            checked_cron = CronScraper(self.username, self.password)

            if not cmd_validated:
                self.cron_action_text.value += (f"\nCommand {command} not available")
                self.page.update()
                deleted_cron = checked_cron.unvalidated_cron_delete(id)
                self.unvalid_found = True
                continue

            checked_cron.send_cron_validation(id)

            # create cron script
            new_cron_script = CronosScript(id)
            new_cron_script.create_script(cmd)

            self.cron_script_path = new_cron_script.script_path

            # add cron to local crontab
            new_cron = local_crons.new(
                command=self.cron_script_path,
                comment=f"{self.COMMENT}-{id}"
            )
            r_cron_str = self.remote_cron_to_str(r_cron)
            new_cron.setall(r_cron_str.split(" ")[:5])
            local_crons.write()
            print(f"{new_cron} : added")

            self.all_msg_in_app.append(new_cron)

            msg = f"\nCron n°{id} // Command <{command}> : added"
            self.cron_action_text.value += msg
            self.page.update()

    # DEL CRON
    # =========================================================================

    def del_local_crons(self) -> None:
        """ Delete local crons that are not in remote crontab """
        remote_crons, local_crons = self.crons_lists()
        crons_to_remove = []

        for l_cron in local_crons:
            if not l_cron.comment:
                continue

            if self.COMMENT not in l_cron.comment:
                continue

            l_cron_id = l_cron.comment.split("-")[1]

            # check if cron still exists on remote
            if any(l_cron_id == str(r_cron["id"]) for r_cron in remote_crons):
                continue

            crons_to_remove.append(l_cron)

        # remove crons
        for cron in crons_to_remove:
            # remove script
            script_id = cron.comment.split("-")[1]
            script_to_delete = CronosScript(script_id)
            script_to_delete.remove_script()

            # remove cron
            local_crons.remove(cron)
            print(f"{cron} : removed")

            self.all_msg_in_app.append(cron)

            id = cron.comment.split("-")[1]
            script = os.path.basename(cron.command)
            command = script.split("-")[1]

            msg = (f"\nCron n°{id} // Command <{command}> : removed")

            self.cron_action_text.value += msg
            self.page.update()

        local_crons.write()

    # PAUSE CRON
    # =========================================================================

    def toggle_pause_local_crons(self) -> None:
        """ Toggle pause/enable on local crons """
        remote_crons, local_crons = self.crons_lists()

        local_crons_dict = {
            cron.comment.split("-")[1]: cron for cron in local_crons
            if cron.comment.split("-")[0] == self.COMMENT
        }

        for r_cron in remote_crons:
            id = str(r_cron["id"])

            if id in local_crons_dict.keys():
                cron = local_crons_dict[id]
                is_paused = r_cron["is_paused"]
                is_enabled = cron.is_enabled()

                if is_paused and is_enabled:
                    cron.enable(False)
                    print(f"{cron} : paused")

                    self.all_msg_in_app.append(cron)

                    self.cron_action_text.value += (f"\nCron n°{cron.comment.split('-')[1]} : paused")
                    self.page.update()

                elif not is_paused and not is_enabled:
                    cron.enable(True)
                    print(f"{cron} : enabled")

                    self.all_msg_in_app.append(cron)

                    self.cron_action_text.value += (f"\nCron n°{cron.comment.split('-')[1]} : enabled")
                    self.page.update()

        local_crons.write()

    # LOGIN
    # =========================================================================

    def login(self) -> None:
        """ Login and fetch remote crons """
        self.elements.fetch_button.text = "Stop Auto-fetch"
        self.authenticate()
        messages_user = self.all_msg_in_app

        if len(messages_user) == 0:
            self.cron_action_text.value = "Nothing to fetch at login"
        self.page.update()

        self.auto_fetch_loop()
        self.all_msg_in_app.clear()

    # AUTO FETCH
    # =========================================================================

    def auto_fetch_on_off(self) -> None:
        """ Fetch remote crons and update local crontab """
        self.auto_fetch = not self.auto_fetch

        if self.auto_fetch:
            self.elements.fetch_button.text = "Stop Auto-fetch"
            self.cron_action_text.value += "\nAuto fetch crons : ON"
        else:
            self.elements.fetch_button.text = "Start Auto-fetch"
            self.cron_action_text.value += "\nAuto fetch crons : OFF"

        messages_user = self.all_msg_in_app

        if (len(messages_user) == 0 and
            not self.unvalid_found and
            self.auto_fetch
            ):
            self.cron_action_text.value += "\nNothing to fetch"
            self.page.update()

        self.auto_fetch_loop()
        self.page.update()

        self.all_msg_in_app.clear()
        self.unvalid_found = False

    # CLEAR MSG
    # =========================================================================

    def clear_msg(self):
        """ Clear all messages in app """
        self.cron_action_text.value = "--Logs cleared--"
        self.page.update()
        time.sleep(2)
        self.cron_action_text.value = ""
        self.page.update()

    # AUTO FETCH LOOP
    # =========================================================================

    def auto_fetch_loop(self):
        """ Auto-fetch remote crons """
        while self.auto_fetch:
            self.add_remote_crons_to_local()
            self.del_local_crons()
            self.toggle_pause_local_crons()
            time.sleep(5)
