import sys
from collections import defaultdict
records = defaultdict(list)
new_records = defaultdict(list)


def hms_to_secs(hours, minutes, seconds):
    return hours * 60 * 60 + minutes * 60 + seconds

def seconds_to_hms(seconds):
    minutes_seconds = divmod(seconds, 60)
    hours_minutes = divmod(minutes_seconds[0], 60)
    return hours_minutes[0], hours_minutes[1], minutes_seconds[1]


def time_stamp_in_hms(hours, minutes, seconds):
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def check_and_adjust_times():
    start_ok = print(f'The first quiz start currently starts at ' +
                     f'''{records['start'][0][0]:02d}:''' +
                     f'''{records['start'][0][1]:02d}:''' + 
                     f'''{records['start'][0][2]:02d}''')

    new_start_input = input(f'What is the correct start time? (hh:mm:ss) ')
    new_start_time = tuple(int(i) for i in new_start_input.replace('\n', '').split(':'))
    new_start_time_in_secs = hms_to_secs(*new_start_time)
    old_start_time_in_secs = hms_to_secs(*records['start'][0])
        
    offset = new_start_time_in_secs - old_start_time_in_secs

    for i in records['start']:
        new_time_in_secs = max(hms_to_secs(*i) + offset, 0)
        new_time_in_hms = seconds_to_hms(new_time_in_secs)
        new_records['start'].append(new_time_in_hms)
        
    for i in records['end']:
        new_time_in_secs = max(hms_to_secs(*i) + offset, 0)
        new_time_in_hms = seconds_to_hms(new_time_in_secs)
        new_records['end'].append(new_time_in_hms)
        
    return new_records


    
def run():
    if len(sys.argv) != 2:
        print('Usage: python3 offset_times.py file.txt')
        sys.exit(1)
    with open(str(sys.argv[1])) as file:
        for line in file:
            quiz_number, start_time, end_time, check = line.split(';')
            print(f'{quiz_number}: start: {start_time} end: {end_time} {check}', end='')
            records['start'].append(tuple(int(i) for i in start_time.split(':')))
            records['end'].append(tuple(int(i) for i in end_time.split(':')))
        print(records)
    new_records = check_and_adjust_times()
    
    print('The new times are:')
    for i in range(len(new_records['start'])):
        print(f'''{i+1} start: {time_stamp_in_hms(*new_records['start'][i])} ''' +
             f'''end: {time_stamp_in_hms(*new_records['end'][i])})''')
        
    confirm = input('Is this right? (y,n) ')
    if confirm.lower() == 'y':
        filename = f'updated_{sys.argv[1]}'
        with open(filename, 'w') as file:
            for i in range(len(new_records['start'])):
                file.write(f'{i+1};' + time_stamp_in_hms(*new_records['start'][i]) + ';' + 
                       time_stamp_in_hms(*new_records['end'][i]) + '\n')
    print(f'File written to {filename}.')

if __name__ == '__main__':
    run()
    
    
