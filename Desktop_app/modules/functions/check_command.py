import shutil


class CheckCommand:
    """ Check if the command is available on the computer """
    def __init__(self, command) -> None:
        """ Initialize the command """
        self.command = command


    @staticmethod
    def is_command_available_unix(command) -> bool:
        """ Check if the command is available on Unix systems """
        return shutil.which(command) is not None
