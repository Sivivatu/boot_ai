# create tests for the functions directory
import os
import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

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

class TestWriteFile(unittest.TestCase):
    def setUp(self):
        self.working_directory = os.getcwd()  # Use the current working directory for testing

    def test_write_lorem_txt(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)  # Print the result to the console
        self.assertIn('28 characters written', result)
        # self.assertIn('Successfully wrote to "lorem.txt"', result)

    def test_write_morelorem_txt(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)  # Print the result to the console
        self.assertIn('26 characters written', result)
        # self.assertIn('Successfully wrote to "pkg/morelorem.txt"', result)

    def test_write_outside_directory(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)  # Print the result to the console
        expected_error = 'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)


class TestRunPythonFile(unittest.TestCase):
    def test_run_main_py(self):
        result = run_python_file("calculator", "main.py")
        print(result)  # Print the result to the console
        self.assertIn("Calculator App", result)
        self.assertFalse(result.startswith("Error:"))
    
    def test_run_main_py_with_args(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)  # Print the result to the console
        self.assertIn("STDOUT:", result)
        self.assertIn("8", result)
        self.assertFalse(result.startswith("Error:"))

    def test_run_tests_py(self):
        result = run_python_file("calculator", "tests.py")
        print(result)  # Print the result to the console
        self.assertIn("STDOUT:", result)
        # self.assertIn("OK", result)
        # self.assertFalse(result.startswith("Error:"))

    def test_run_outside_directory(self):
        result = run_python_file("calculator", "../main.py")
        print(result)  # Print the result to the console
        self.assertIn("Error: Cannot execute", result)

    def test_run_nonexistent_file(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result)  # Print the result to the console
        self.assertIn("Error: File \"nonexistent.py\" not found", result)

    def test_run_lorem_txt(self):
        result = run_python_file("calculator", "lorem.txt")
        print(result)  # Print the result to the console
        self.assertIn("Error: File \"lorem.txt\" is not a Python file", result)


if __name__ == "__main__":
    unittest.main()