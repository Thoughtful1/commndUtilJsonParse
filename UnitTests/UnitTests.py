import ConsoleUtility
import unittest
import sys


class TestStringMethods(unittest.TestCase):
    path_to_files_saving = ""
    files_count = 1
    file_name = "example"
    file_prefix = "random"
    data_schema = ""
    data_linesBool = False
    clear_pathBool = False

    name = ConsoleUtility.generate_uuid()

    def test_validate_suffix_adder(self):
        self.assertEqual(ConsoleUtility.file_prefix_adder('random'), 'random')

    def test_validate_value(self):
        self.assertEqual(ConsoleUtility.validate_count_value(2), 2)
        self.assertEqual(ConsoleUtility.validate_count_value('placeholder'), 0)

    def test_check_config(self):
        self.assertEqual(ConsoleUtility.check_if_config_exist(), False)

    def test_json_recognicnition(self):
        json_placeholder='{"date": 1632494625.0943308, "name": "bd702acc-c80b-4df7-b2aa-a9eb88f8caa3", "type": "client", "age": "int.rand:81"}'
        ConsoleUtility.check_data_schema(json_placeholder, self.path_to_files_saving, self.file_name, self.file_prefix)


if __name__ == '__main__':
    unittest.main()
