from optimize import log
import statistics
import random
import os

file_path = str(os.path.dirname(__file__))
name_of_result_file = 'pseudo_file.txt'
test_file = 'test_file.txt'


def teardown():
    log.clean_file(file_path, name_of_result_file)


def test_write_to_file():
    random.seed(1)
    i = 1
    mins = [random.randint(1, 10) for _ in range(10)]
    avgs = [random.randint(1, 10) for _ in range(10)]
    gl_min = min(mins)
    gl_avg = statistics.mean(avgs)
    log.write_to_file(file_path, i, mins, avgs, gl_min, gl_avg, name=name_of_result_file)
    with open(os.path.join(file_path, test_file), 'r') as expected_file:
        expected_file_lines = expected_file.readlines()
    with open(os.path.join(file_path, name_of_result_file), 'r') as actual_file:
        actual_file_lines = actual_file.readlines()
    assert actual_file_lines == expected_file_lines
