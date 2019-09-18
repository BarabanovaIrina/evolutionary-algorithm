from optimize import log
import statistics
import random
from mock import patch
import os

path = './'
name_of_result_file = 'pseudo_file.txt'
file_path = os.path.join(os.path.dirname(__file__), 'test_file.txt')


def write_to_file_test(path, i, list_of_mins, list_of_averages, global_min, global_avg, name='pseudo_file.txt'):
    with open(path+name, 'w') as file:
        file.write(f'History {i}\n'),
        file.write(f'Минимумы всех поколений: {list_of_mins}\n')
        file.write(f'Средние всех поколений: {list_of_averages}\n')
        file.write(f'Глобальный минимум: {global_min}\n')
        file.write(f'Глобальное среднее: {global_avg}\n')


def test_write_to_file():
    random.seed(1)
    i = 1
    mins = [random.randint(1, 10) for _ in range(10)]
    avgs = [random.randint(1, 10) for _ in range(10)]
    gl_min = min(mins)
    gl_avg = statistics.mean(avgs)
    with patch('optimize.log.write_to_file', write_to_file_test(path, i, mins, avgs, gl_min, gl_avg, name=name_of_result_file)):
        with open(file_path, 'r') as expected_file:
            expected_file_lines = expected_file.readlines()
        with open(path+name_of_result_file, 'r') as actual_file:
            actual_file_lines = actual_file.readlines()

        assert actual_file_lines == expected_file_lines
