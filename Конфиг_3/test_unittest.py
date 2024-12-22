import unittest
import os
import tempfile
import subprocess
import sys

class TestPrak3(unittest.TestCase):

    def setUp(self):
        self.sample_json = """{
    "comment1": ["Это однострочный комментарий"],
    "def Constant1": 42,
    "def Constant2": "Привет, мир!",
    "!(Constant2)": null,
    "numbers": [1, 2, 3, 4, 5],
    "strings": ["яблоко", "банан", "вишня"],
    "arrays": [
      [10, 20],
      [30, 40]
    ],
    "dictionary": {
      "key1": "значение1",
      "key2": "значение2",
      "nestedDictionary": {
        "innerKey": "внутреннее_значение"
      }
    },
    "comment2": [
      "Это",
      "многострочный",
      "комментарий"
    ]
}"""

        self.expected_output = """{
    % Это однострочный комментарий
    def Constant1 := 42
    def Constant2 := 'Привет, мир!'
    Constant2 => 'Привет, мир!'
    numbers => [ 1, 2, 3, 4, 5 ]
    strings => [ 'яблоко', 'банан', 'вишня' ]
    arrays => [ [ 10, 20 ], [ 30, 40 ] ]
    dictionary => {
        key1 => 'значение1'
        key2 => 'значение2'
        nestedDictionary => {
            innerKey => 'внутреннее_значение'
        }

    }

    /#
    Это
    многострочный
    комментарий
    #/
}"""

    def test_valid_input(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp_in:
            tmp_in.write(self.sample_json)
            tmp_in_path = tmp_in.name
        tmp_out = tempfile.NamedTemporaryFile(delete=False)
        tmp_out_path = tmp_out.name
        tmp_out.close()

        try:
            result = subprocess.run(
                [sys.executable, "main.py", "-i", tmp_in_path, "-o", tmp_out_path],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            with open(tmp_out_path, 'r', encoding='utf-8') as f:
                output_content = f.read()
            self.assertEqual(output_content.strip(), self.expected_output.strip())
        finally:
            os.remove(tmp_in_path)
            os.remove(tmp_out_path)

    def test_file_not_found(self):
        # Предполагаем, что код завершится с ошибкой
        tmp_out = tempfile.NamedTemporaryFile(delete=False)
        tmp_out_path = tmp_out.name
        tmp_out.close()
        try:
            result = subprocess.run(
                [sys.executable, "main.py", "-i", "nonexistent.json", "-o", tmp_out_path],
                capture_output=True, text=True
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Input file not found", result.stdout + result.stderr)
        finally:
            os.remove(tmp_out_path)

    def test_invalid_json(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp_in:
            tmp_in.write("{ invalid json")
            tmp_in_path = tmp_in.name
        tmp_out = tempfile.NamedTemporaryFile(delete=False)
        tmp_out_path = tmp_out.name
        tmp_out.close()

        try:
            result = subprocess.run(
                [sys.executable, "main.py", "-i", tmp_in_path, "-o", tmp_out_path],
                capture_output=True, text=True
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Syntax error in JSON input", result.stdout + result.stderr)
        finally:
            os.remove(tmp_in_path)
            os.remove(tmp_out_path)

if __name__ == "__main__":
    unittest.main()