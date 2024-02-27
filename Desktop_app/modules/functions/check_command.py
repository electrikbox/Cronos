"""Function that check if the received command
exist and can be executed on the computer"""

import shutil


class CheckCommand:
    def __init__(self, command) -> None:
        self.command = command

    # Linux - Mac OS
    # =============================================================================

    @staticmethod
    def is_command_available_unix(command) -> bool:
        return shutil.which(command) is not None


if __name__ == "__main__":
    print(CheckCommand.is_command_available_unix("cal"))
