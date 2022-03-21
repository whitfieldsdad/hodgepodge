from unittest import TestCase
from hodgepodge.processes import Process

import hodgepodge.commands


class CommandExecutionTestCases(TestCase):
    def test_execute_command(self):
        result = hodgepodge.commands.execute_command('hostname')
        self.assertIsInstance(result, Process)
        self.assertEqual(0, result.exit_code)
