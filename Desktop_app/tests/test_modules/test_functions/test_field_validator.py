import unittest
from unittest.mock import MagicMock
from modules.functions.field_validator import validate

class TestFieldValidator(unittest.TestCase):
    def test_validate(self):
        # Create mock objects
        elements = MagicMock()
        page = MagicMock()

        # Set mock values
        elements.username_field.value = "username"
        elements.password_field.value = "password"

        # Call the function to be tested
        validate(elements, page)

        # Assert that the login button is enabled
        self.assertFalse(elements.login_button.disabled)

        # Assert that the page is updated
        page.update.assert_called_once()
        