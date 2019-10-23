import os


def clean_file(path, name='file.txt'):
    with open(os.path.join(path, name), 'w') as file:
        file.seek(0)


def write_to_file(path, i, list_of_mins, list_of_averages, global_min, global_avg, name='history.txt'):
    with open(os.path.join(path, name), 'a') as file:
        file.write(f'History {i}\n'),
        file.write(f'Mins through the history: {list_of_mins}\n')
        file.write(f'Avgs through the history: {list_of_averages}\n')
        file.write(f'Global min: {global_min}\n')
        file.write(f'Global avg: {global_avg}\n')


def write_run_params(path, data, file_name='optimization_params.txt'):
    with open(os.path.join(path, file_name), 'a') as file:
        for key in data.keys():
            file.write(f'{key}: {data[key].__name__}\n')
