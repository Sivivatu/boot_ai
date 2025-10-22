# create tests for the functions directory
import os
import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

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


class TestGetFileContent(unittest.TestCase):
    def test_get_file_content_main_py(self):
        # Test reading calculator/main.py
        result = get_file_content("calculator", "main.py")
        print(result)  # Print the result to the console
        self.assertIn("import sys", result)
        self.assertIn("Calculator", result)
        self.assertFalse(result.startswith("Error:"))
    
    def test_get_file_content_pkg_calculator_py(self):
        # Test reading calculator/pkg/calculator.py
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)  # Print the result to the console
        self.assertIn("class Calculator", result)
        self.assertFalse(result.startswith("Error:"))
    
    def test_get_file_content_outside_directory(self):
        # Test reading /bin/cat which is outside the working directory
        result = get_file_content("calculator", "/bin/cat")
        print(result)  # Print the result to the console
        expected_error = 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)
    
    def test_get_file_content_non_existent(self):
        # Test reading a non-existent file
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        print(result)  # Print the result to the console
        expected_error = 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
        self.assertEqual(result, expected_error)


if __name__ == "__main__":
    unittest.main()