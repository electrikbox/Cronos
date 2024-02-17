import os
import stat
import platform

CRONOS_SCRIPT_PATH = os.path.expanduser("~/cronos_scripts")

class CronosScript:

    def __init__(self, cron_id: int) -> None:
        self.cron_id = cron_id
        self.script_path = ""

    def create_script(self, cmd: str) -> None:
        os_name = platform.system()
        folder_path = os.path.expanduser(CRONOS_SCRIPT_PATH)
        option = ""
        cmd_name = cmd.split(" ")[0]

        if os_name == "Linux" and cmd_name == "open":
            option = "export DISPLAY=:0\n"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        script = os.path.join(folder_path, f"cron_{self.cron_id}_script.sh")
        script_content = f"#!/bin/bash\n{option}{cmd}"

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



# if __name__ == "__main__":
    # cron = CronosScript(234, "cp /home/electrik/Bureau/from/test_file /home/electrik/Bureau/to/test_file")
    # cron.create_script()
    # cron.remove_script()
