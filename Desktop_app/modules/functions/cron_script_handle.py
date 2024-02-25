import os
import stat
import platform

USER_PATH = os.path.expanduser("~")
CRONOS_SCRIPT_PATH = os.path.expanduser("~/cronos_scripts")
CRONOS_COPY_FOLDER = "Cronos_copy_folder"


class CronosScript:

    def __init__(self, cron_id: int) -> None:
        self.cron_id = cron_id
        self.script_path = ""

    def build_script(self, cmd: str) -> str:
        os_name = platform.system()
        option = ""
        cmd_name = cmd.split(" ")[0]

        if os_name == "Linux" and cmd_name == "open":
            option = "export DISPLAY=:0\n"

        elif cmd_name == "cp":
            source = cmd.split(" ")[1]
            destination = cmd.split(" ")[2]

            destination_path = os.path.join(USER_PATH, CRONOS_COPY_FOLDER, destination)
            var_dest = f'destination="{destination_path}"'

            check_dest = f'if [ ! -d "$destination" ]; then\n\tmkdir -p "$destination"\nfi\n'
            option = f"{var_dest}\n{check_dest}\n"

            exclude = f"-path \'{destination_path}\' -prune -o"
            search_file = f"-iname \"{source}\""
            exec_copy = f"-exec cp -t \"$destination\" -r {{}} +"

            cmd = f'find {USER_PATH} {exclude} {search_file} {exec_copy}'

        script_shibang = "#!/bin/bash\n"
        script_protect_sudo = '\nif [ $(id -u) -eq 0 ];\n\tthen echo "sudo forbiden."\n\texit 1\nfi\n'
        script_content = f"{script_shibang}{script_protect_sudo}{option}{cmd}"

        return script_content

    def create_script(self, cmd: str) -> None:
        folder_path = os.path.expanduser(CRONOS_SCRIPT_PATH)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        script = os.path.join(folder_path, f"cron_{self.cron_id}_script.sh")
        script_content = self.build_script(cmd)

        with open(script, "w") as f:
            f.write(script_content)

        os.chmod(script, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        self.script_path = script

    def remove_script(self) -> None:
        folder_path = os.path.expanduser(CRONOS_SCRIPT_PATH)
        script = os.path.join(folder_path, f"cron_{self.cron_id}_script.sh")
        self.script_path = script

        if os.path.exists(script):
            os.remove(script)
