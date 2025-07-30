# create tests for the functions/get_files_info.py script
import unittest
import os
from functions.get_files_info import get_files_info 

class TestGetFilesInfo(unittest.TestCase):
    def setUp(self):
        self.working_directory = os.getcwd()  # Use the current working directory for testing

    def test_get_files_info_calculator_directory(self):
        # Run get_files_info on the 'calculator' directory from the workspace root
        result = get_files_info("calculator", ".")
        print(result)  # Print the result to the console
        # Check that the expected files and directories are listed
        self.assertIn("main.py", result)
        self.assertIn("tests.py", result)
        self.assertIn("pkg", result)
        # Optionally check for file_size and is_dir info
        self.assertIn("file_size=", result)
        self.assertIn("is_dir=", result)
        
    def test_get_files_info_parent_directory(self):
        # Run get_files_info on the '../' directory from the 'calculator' working directory
        result = get_files_info("calculator", "../")
        print(result)  # Print the result to the console
        expected_error = 'Error: Cannot list "../" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)

    def test_get_files_info_bin_directory(self):
        # Run get_files_info on the '/bin' directory from the 'calculator' working directory
        result = get_files_info("calculator", "/bin")
        print(result)  # Print the result to the console
        expected_error = 'Error: Cannot list "/bin" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)


    # def test_get_files_info_invalid_directory(self):
    #     invalid_directory = "/invalid/directory/path"
    #     result = get_files_info(self.working_directory, invalid_directory)
    #     self.assertEqual(result, f'Error: Cannot list "{invalid_directory}" as it is outside the permitted working directory')

    # def test_get_files_info_non_existent_directory(self):
    #     non_existent_directory = os.path.join(self.working_directory, "non_existent")
    #     result = get_files_info(self.working_directory, non_existent_directory)
    #     self.assertEqual(result, f'Error: "{non_existent_directory}" is not a directory')

if __name__ == "__main__":
    unittest.main()