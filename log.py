def clean_file(path):
    with open(path+'file.txt', 'w') as file:
        file.seek(0)


def write_to_file(path, i, list_of_mins, list_of_averages, global_min, global_avg):
    with open(path+'file.txt', 'a') as file:
        file.write(f'History {i}\n'),
        file.write(f'Минимумы всех поколений: {list_of_mins}\n')
        file.write(f'Средние всех поколений: {list_of_averages}\n')
        file.write(f'Глобальный минимум: {global_min}\n')
        file.write(f'Глобальное среднее: {global_avg}\n')