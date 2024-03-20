import os
import stat
import platform

USER_PATH = os.path.expanduser("~")
CRONOS_PATH = os.path.expanduser("~/Cronos")

CRONOS_SCRIPT_PATH = f"{CRONOS_PATH}/.cronos_scripts"
CRONOS_COPY_FOLDER = f"{CRONOS_PATH}/Cronos_copy"
CRONOS_LIST_FOLDER = f"{CRONOS_PATH}/Cronos_list"

SCRIPT_SHEBANG = "#!/bin/bash\n"
SCRIPT_PREVENT_SUDO = ('\nif [ $(id -u) -eq 0 ];\n\tthen echo "sudo forbiden."\n\texit 1\nfi\n')


class CronosScript:
    """ Represents a cron script handler """

    def __init__(self, cron_id: int) -> None:
        """ Initialize the cron script handler """
        self.cron_id = cron_id
        self.script_path = ""

    # TOOLS for cmd (ls + cp)
    # =========================================================================

    def utils_ls_cp(self, cmd: str, folder: str) -> dict[str, str]:
        """ Return option, exclude, search_file and destination_path """
        source = cmd.split(" ")[1]
        destination = cmd.split(" ")[2]

        destination_path = os.path.join(folder, destination)
        var_dest = f'destination="{destination_path}"'

        # Create destination if not exists
        check_dest = (f'if [ ! -d "$destination" ]; then\n\tmkdir -p "$destination"\nfi\n')
        option = f"{var_dest}\n{check_dest}\n"

        # Exclude destinatin folder from search
        # exclude = f'-path "{CRONOS_PATH}" -prune -o'
        exclude = f'-path "{CRONOS_PATH}" -o'
        search_file = f'-iname "{source}"'

        return {
            "option": option,
            "exclude": exclude,
            "search_file": search_file,
            "destination_path": destination_path,
        }

    # Open command
    # =========================================================================

    def open_command(self, cmd: str) -> tuple[str, str]:
        """ Returns the option and the command for the open command """
        os_name = platform.system()
        option = ""

        if os_name == "Linux":
            option = "export DISPLAY=:0\n"

        return (option, cmd)

    # Copy command
    # =========================================================================

    def copy_command(self, cmd: str) -> tuple[str, str]:
        """ Returns the option and the command for the copy command """
        os_name = platform.system()

        utils = self.utils_ls_cp(cmd, CRONOS_COPY_FOLDER)
        option = utils["option"]
        exclude = utils["exclude"]
        search_file = utils["search_file"]

        if os_name == "Linux":
            exec_copy = f'-exec cp -t "$destination" -r {{}} +'
        else:
            exec_copy = f'-exec cp -R {{}} "$destination" \;'

        cmd = f"find {USER_PATH} {exclude} {search_file} {exec_copy}"

        return (option, cmd)

    # List command
    # =========================================================================

    def list_command(self, cmd: str) -> tuple[str, str]:
        """ Returns the option and the command for the copy command """
        file = cmd.split(" ")[1].split(".")[0]

        utils = self.utils_ls_cp(cmd, CRONOS_LIST_FOLDER)
        option = utils["option"]
        option += 'current_date=$(date +"%Y-%m-%d")\n'
        exclude = utils["exclude"]
        search_file = utils["search_file"]
        dest_path = utils["destination_path"]

        exec_copy = (
            f"-exec ls {{}} \; > {dest_path}/list-{file}-$current_date.txt"
        )

        cmd = f"find {USER_PATH} {exclude} {search_file} {exec_copy}"

        return (option, cmd)

    # Build script
    # =========================================================================

    def build_script(self, cmd: str) -> str:
        """ Builds a script content based on the given command """
        option = ""
        cmd_name = cmd.split(" ")[0]

        if cmd_name == "open":
            option, cmd = self.open_command(cmd)

        elif cmd_name == "cp":
            option, cmd = self.copy_command(cmd)

        elif cmd_name == "ls":
            option, cmd = self.list_command(cmd)

        script_content = f"{SCRIPT_SHEBANG}{SCRIPT_PREVENT_SUDO}{option}{cmd}"

        return script_content

    # Create script
    # =========================================================================

    def create_script(self, cmd: str) -> None:
        """ Creates a cron script file with the given command """
        folder_path = os.path.expanduser(CRONOS_SCRIPT_PATH)
        cmd_name = cmd.split(" ")[0]

        # Create folder if not exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Script name
        script = os.path.join(folder_path, f"cron_{self.cron_id}-{cmd_name}-script.sh")
        # Script content
        script_content = self.build_script(cmd)

        with open(script, "w") as f:
            f.write(script_content)

        os.chmod(script, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        # os.chmod(script, stat.S_IXUSR)
        self.script_path = script

    # Remove script
    # =========================================================================

    def remove_script(self) -> None:
        """ Removes the script file associated with the cron job """
        folder_path = os.path.expanduser(CRONOS_SCRIPT_PATH)

        for filename in os.listdir(folder_path):
            if str(self.cron_id) in filename:
                script = os.path.join(folder_path, filename)

        self.script_path = script

        if os.path.exists(script):
            os.remove(script)
