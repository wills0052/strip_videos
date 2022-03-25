import sys, os, re
from collections import defaultdict
from itertools import product
from pathlib import Path



def hms_to_secs(hours, minutes, seconds):
    return hours * 60 * 60 + minutes * 60 + seconds

def secs_to_hms(seconds):
    mins_secs = divmod(seconds, 60)
    hours_mins = divmod(mins_secs[0], 60)
    return hours_mins[0], hours_mins[1], mins_secs[1]

def time_stamp_in_hms(hours, minutes, seconds):
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def get_durations_in_secs(records):
    durations = []
    for i in range(len(records['start'])):
        start_time_in_secs = hms_to_secs(*records['start'][i])
        end_time_in_secs = hms_to_secs(*records['end'][i])
        durations.append(end_time_in_secs - start_time_in_secs)
    return durations
        
def check_and_adjust_lengths(records, durations):
    new_records = defaultdict(list)
    for i in range(len(durations)):
        duration_in_hms = secs_to_hms(durations[i])
        print(f'Quiz {i+1} is {duration_in_hms[0]:02d}:{duration_in_hms[1]:02d}:' + 
                f'{duration_in_hms[2]:02d} long.')
    while True:
        try:
            durations_correct = input(f'Are these durations fine? (y or Enter/n) [e to exit] ').lower()
            if durations_correct == 'e':
                print('Exiting.')
                sys.exit(1)
            elif durations_correct == 'y' or not durations_correct:
                print('Durations correct. Proceeding.')
                return records
            elif durations_correct == 'n':
                break
            else:
                raise ValueError
        except ValueError:
            print('Invalid input.')
    # Ask for new max duration
    while True:
        try:
            new_max_duration = input(f'What is the maximum duration? (hh:mm:ss) [Enter for default 00:05:00, e to exit] ').lower()
            if new_max_duration == 'e':
                print('Exiting.')
                sys.exit(1)
            elif not new_max_duration:
                print('Selected 00:05:00.')
                new_max_duration = hms_to_secs(0,5,0)
                break
            elif not re.search('^\d{2}:\d{2}:\d{2}$', new_max_duration):
                raise ValueError
            new_max_duration = hms_to_secs(*(int(i) \
                                                 for i in new_max_duration.replace('\n', '').split(':')))
            break
        except ValueError:
            print('Invalid input')

    # Fix new times     
    for i in range(len(records['start'])):
        new_records['start'].append(records['start'][i])
        start_time_in_secs = hms_to_secs(*records['start'][i])
        end_time_in_secs = hms_to_secs(*records['end'][i])
        new_difference_in_secs = min(end_time_in_secs - start_time_in_secs, \
                                     new_max_duration)
        new_records['end'].append(secs_to_hms(start_time_in_secs + \
                                                 new_difference_in_secs))
        new_records['check'].append(records['check'][i])
        
    return new_records
    

def check_and_adjust_start_times(records):
    new_records = defaultdict(list)
    # Print start times
    start_ok = print(f'The first quiz start currently starts at ' +
                     f'''{records['start'][0][0]:02d}:''' +
                     f'''{records['start'][0][1]:02d}:''' + 
                     f'''{records['start'][0][2]:02d}''')

    # Check for start time
    while True:
        try:
            times_correct = input(f'Is this start time correct? (y or Enter/n) [e to exit] ')
            if times_correct.lower() == 'e':
                print('Exiting.')
                sys.exit(1)
            elif times_correct.lower() == 'y' or not times_correct:
                print('Times correct. Proceeding.')
                return records
            elif times_correct.lower() == 'n':
                break
            else:
                raise ValueError
        except ValueError:
            print('Invalid input.')
            
    
    # Ask for new start times
    while True:
        try:
            new_start_input = input(f'What is the correct start time? (hh:mm:ss) [e to exit] ')
            if new_start_input.lower() == 'e':
                print('Exiting.')
                sys.exit(1)
            if not re.search('^\d{2}:\d{2}:\d{2}$', new_start_input):
                raise ValueError
            new_start_time = tuple(int(i) for i in new_start_input.replace('\n', '').split(':'))
            break
        except ValueError:
            print('Invalid input')
    new_start_time_in_secs = hms_to_secs(*new_start_time)
    old_start_time_in_secs = hms_to_secs(*records['start'][0])
        
    offset = new_start_time_in_secs - old_start_time_in_secs

    # Fix new times
    for i in range(len(records['start'])):
        new_time_in_secs = max(hms_to_secs(*records['start'][i]) + offset, 0)
        new_time_in_hms = secs_to_hms(new_time_in_secs)
        new_records['start'].append(new_time_in_hms)
        new_records['check'].append(records['check'][i])
        
    for i in range(len(records['end'])):
        new_time_in_secs = max(hms_to_secs(*records['end'][i]) + offset, 0)
        new_time_in_hms = secs_to_hms(new_time_in_secs)
        new_records['end'].append(new_time_in_hms)
    
    return new_records


def process_file():
    records = defaultdict(list)
    # head, filename = os.path.split(sys.argv[1])
    file_location = Path(sys.argv[1])
    if len(sys.argv) != 2 or sys.argv[1][-3:] != 'vtt':
        print('Usage: python3 offset_times.py transcript.vtt')
        sys.exit(1)
    if os.stat(file_location).st_size == 0:
        print('No times detected.')
        sys.exit(1)
        

    with open(file_location) as file:
        print('Current quiz times are:')
        for line in file:
            try:
                quiz_number, start_time, end_time, check = line.split(';')
                records['start'].append(tuple(int(i) for i in start_time.split(':')))
                records['end'].append(tuple(int(i) for i in end_time.split(':')))
                records['check'].append(check)
                print(f'{int(quiz_number):2d}: {start_time} -- {end_time} {check}', end='')
            except ValueError:
                print('Invalid input file. Check it has been processed by find_quiz_times.py and is of the form #;hh:mm:ss;hh:mm:ss; \n')
                sys.exit(1)
            
    return records
     
def check_records_equal(records1, records2):
    
    for i in range(len(records1['start'])):
        for j in range(3):
            if records1['start'][i][j] != records2['start'][i][j] or \
                records1['end'][i][j] != records2['end'][i][j]:
                return False
    return True
 
    
    
def verify_new_times(records, new_records, durations, new_durations):
    duration_in_hms = [secs_to_hms(i) for i in durations]
    new_duration_in_hms = [secs_to_hms(i) for i in new_durations]
    print(duration_in_hms)
    print('New quiz times are:')
    for i in range(len(new_records['start'])):
        print(f'''{i+1:2d}: {time_stamp_in_hms(*new_records['start'][i])} -- ''' +
             f'''{time_stamp_in_hms(*new_records['end'][i])}, '''
             f'''duration: {new_duration_in_hms[i][0]:02d}:{new_duration_in_hms[i][1]:02d}:''' + 
                f'''{new_duration_in_hms[i][2]:02d}, {records['check'][i]}''', end='')
    print()
    print('Old quiz times were:')
    for i in range(len(new_records['start'])):
        print(f'''{i+1:2d}: {time_stamp_in_hms(*records['start'][i])} -- ''' +
             f'''{time_stamp_in_hms(*records['end'][i])} '''
             f'''duration: {duration_in_hms[i][0]:02d}:{duration_in_hms[i][1]:02d}:''' + 
                f'''{duration_in_hms[i][2]:02d}, {records['check'][i]}''', end='')
    confirm = input('Is this right? (y,n) [e to exit] ')
    if confirm.lower() == 'e':
        print('Exiting.')
        sys.exit(1)
    if confirm.lower() == 'y':
        return new_records
    return records

def write_to_file(new_records):
    
    filename = sys.argv[1]
    with open(filename, 'w') as file:
        for i in range(len(new_records['start'])):
            file.write(f'{i+1};' + time_stamp_in_hms(*new_records['start'][i]) + ';' + 
                   time_stamp_in_hms(*new_records['end'][i]) + ';' + new_records['check'][i])
    print(f'File written to {filename}.')    
    
def run():
    records = process_file()
    duration_triggering_flag = 5*60
    duration_trigger_string = f'{secs_to_hms(duration_triggering_flag)[0]:02d}:' + \
                                f'{secs_to_hms(duration_triggering_flag)[1]:02d}:' + \
                                f'{secs_to_hms(duration_triggering_flag)[2]:02d}'
    durations = get_durations_in_secs(records)
    if any(i for i in durations if i > duration_triggering_flag):
        print(f'''Detected duration greater than {duration_trigger_string}''')
        new_records = check_and_adjust_lengths(records, durations)
        new_durations = get_durations_in_secs(new_records)
        new_records = verify_new_times(records, new_records, durations, new_durations)
        records = new_records
        
    # Allow for adjusting start times
    new_records = check_and_adjust_start_times(records)
    while not check_records_equal(records, new_records):
        print(records)
        new_durations = get_durations_in_secs(new_records)
        durations = get_durations_in_secs(records)
        new_records = verify_new_times(records, new_records, durations, new_durations)
        new_records = check_and_adjust_start_times(records)

    write_to_file(new_records)
    return 0

if __name__ == '__main__':
    run()

