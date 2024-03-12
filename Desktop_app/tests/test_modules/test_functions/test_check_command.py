import unittest
from unittest.mock import patch
from modules.functions.check_command import CheckCommand

class TestCheckCommand(unittest.TestCase):
    """ Test CheckCommand class """
    def test_is_command_available_unix(self):
        """ Test is_command_available_unix method """
        with patch("shutil.which") as mock_which:
            # Command is available
            mock_which.return_value = "/usr/bin/command"
            result = CheckCommand.is_command_available_unix("command")
            self.assertTrue(result)

            # Command is not available
            mock_which.return_value = None
            result = CheckCommand.is_command_available_unix("command")
            self.assertFalse(result)

    def test_init(self):
        """ Test __init__ method """
        command = "test_command"
        check_command = CheckCommand(command)
        self.assertEqual(check_command.command, command)
