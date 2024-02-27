import flet as ft
import os
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

    # MSG in APP
    # =========================================================================

    def cron_action_msg(self, messages: list[str]):
        combined_msg = "\n".join(messages)
        self.cron_action_text.value = combined_msg
        self.page.update()

    # UTILS
    # =========================================================================

    def remote_cron_to_str(self, cron: dict) -> str:
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
        remote_crons = CronScraper(
            self.username,
            self.password
        ).get_remote_crons(self.token)
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

        added_crons_msg = []

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
                self.all_msg_in_app(f"Command {command} not available")
                deleted_cron = checked_cron.unvalidated_cron_delete(id)
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

            # MSG USER ON APP
            message_user = f"Cron n°{id} // Command <{command}> : added"
            added_crons_msg.append(message_user)

            self.all_msg_in_app.extend(added_crons_msg)

            self.cron_action_msg(self.all_msg_in_app)
            added_crons_msg.clear()


    # DEL CRON
    # =========================================================================

    def del_local_crons(self) -> None:
        remote_crons, local_crons = self.crons_lists()
        crons_to_remove = []

        removed_crone_msg = []

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

            # MSG USER ON APP
            removed_msg = f"Cron n°{cron.comment.split('-')[1]} // Script {os.path.basename(cron.command)} : removed"
            removed_crone_msg.append(removed_msg)

        self.all_msg_in_app.extend(removed_crone_msg)
        self.cron_action_msg(self.all_msg_in_app)

        local_crons.write()


    # PAUSE CRON
    # =========================================================================

    def toggle_pause_local_crons(self) -> None:
        remote_crons, local_crons = self.crons_lists()

        local_crons_dict = {
            cron.comment.split("-")[1]: cron for cron in local_crons
            if cron.comment.split("-")[0] == self.COMMENT
        }

        paused_crons_msg = []
        enabled_crons_msg = []

        for r_cron in remote_crons:
            id = str(r_cron["id"])

            if id in local_crons_dict.keys():
                cron = local_crons_dict[id]
                is_paused = r_cron["is_paused"]
                is_enabled = cron.is_enabled()

                if is_paused and is_enabled:
                    cron.enable(False)
                    print(f"{cron} : paused")
                    # MSG USER ON APP
                    message = f"Cron n°{cron.comment.split('-')[1]} : paused"
                    paused_crons_msg.append(message)
                elif not is_paused and not is_enabled:
                    cron.enable(True)
                    print(f"{cron} : enabled")
                    # MSG USER ON APP
                    message = f"Cron n°{cron.comment.split('-')[1]} : enabled"
                    enabled_crons_msg.append(message)

        self.all_msg_in_app.extend(paused_crons_msg)
        self.all_msg_in_app.extend(enabled_crons_msg)

        self.cron_action_msg(self.all_msg_in_app)

        local_crons.write()

    # MAIN METHODS
    # =========================================================================

    def login(self) -> None:
        self.authenticate()
        self.add_remote_crons_to_local()
        self.del_local_crons()
        self.toggle_pause_local_crons()

        messages = self.all_msg_in_app

        self.cron_action_msg(messages)

    def fetch_remote_crons(self) -> None:
        self.add_remote_crons_to_local()
        self.del_local_crons()
        self.toggle_pause_local_crons()

        # while True:
        #     self.add_remote_crons_to_local()
        #     self.del_local_crons()
        #     self.toggle_pause_local_crons()
        #     time.sleep(5)

        messages = self.all_msg_in_app

        self.cron_action_msg(messages)
