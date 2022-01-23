import unittest
import log_parser.log_parser as lp
import os
import csv


def get_paths(dir):
    return [os.path.join(dir, path) for path in os.listdir(dir)]

INPUT_PATHS = [os.path.join('logs', path) for path in os.listdir('logs')]
OUTPUT_PATHS = [os.path.join('output', path) for path in os.listdir('output')]


class TestParser(unittest.TestCase):
    def test_output_len_matches_unique_minutes(self):
        test_input = INPUT_PATHS[0]
        test_output = OUTPUT_PATHS[0]
        minutes = {item[0] for item in lp.create_tuple_list(test_input)}
        with open(test_output) as f:
            # read header
            f.readline()
            # then count the rest
            file_len = len(f.readlines())
        self.assertEqual(len(minutes), file_len)


    def test_schema_validation(self):
        test_output = OUTPUT_PATHS[0]
        test_header = list(lp.create_row_dict('test').keys())
        with open(test_output) as f:
            reader = csv.reader(f)
            header = next(reader)

        self.assertEqual(test_header, header)


    def test_check_sort_order(self):
        test_output = OUTPUT_PATHS[0]
        with open(test_output) as f:
            reader = csv.DictReader(f)
            minutes = [col['time'] for col in reader]
        
        self.assertEqual(minutes, sorted(minutes))
                

    def test_rows_have_int_vals(self):
        test_output = OUTPUT_PATHS[0]
        empties = False
        with open(test_output) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if any(val in (None, "") for val in row.values()):
                    empties = True
                    break
        self.assertFalse(empties)


if __name__ == '__main__':
    unittest.main()
