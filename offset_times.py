import sys, os, re
from collections import defaultdict



def hms_to_secs(hours, minutes, seconds):
    return hours * 60 * 60 + minutes * 60 + seconds

def seconds_to_hms(seconds):
    minutes_seconds = divmod(seconds, 60)
    hours_minutes = divmod(minutes_seconds[0], 60)
    return hours_minutes[0], hours_minutes[1], minutes_seconds[1]

def time_stamp_in_hms(hours, minutes, seconds):
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def check_and_adjust_times(records):
    new_records = defaultdict(list)
    # Print start times
    start_ok = print(f'The first quiz start currently starts at ' +
                     f'''{records['start'][0][0]:02d}:''' +
                     f'''{records['start'][0][1]:02d}:''' + 
                     f'''{records['start'][0][2]:02d}''')

    # Check for start time
    while True:
        try:
            times_correct = input(f'Are these times correct? (y/n) [e to exit] ')
            if times_correct.lower() == 'e':
                print('Exiting.')
                sys.exit(1)
            elif times_correct.lower() == 'y':
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
    for i in records['start']:
        new_time_in_secs = max(hms_to_secs(*i) + offset, 0)
        new_time_in_hms = seconds_to_hms(new_time_in_secs)
        new_records['start'].append(new_time_in_hms)
        
    for i in records['end']:
        new_time_in_secs = max(hms_to_secs(*i) + offset, 0)
        new_time_in_hms = seconds_to_hms(new_time_in_secs)
        new_records['end'].append(new_time_in_hms)
        
    return new_records


def process_file():
    records = defaultdict(list)
    head, filename = os.path.split(sys.argv[1])
    print(sys.argv[1])
    if len(sys.argv) != 2:
        print('Usage: python3 offset_times.py transcript.vtt')
        sys.exit(1)
    if os.stat(filename).st_size == 0:
        print('No times detected.')
        sys.exit(1)
    with open(str(sys.argv[1])) as file:

            
        print('Current quiz times are:')
        for line in file:
            quiz_number, start_time, end_time, check = line.split(';')
            records['start'].append(tuple(int(i) for i in start_time.split(':')))
            records['end'].append(tuple(int(i) for i in end_time.split(':')))
            print(f'{int(quiz_number):2d}: {start_time} -- {end_time} {check}', end='')
            
    return records
     
def check_records_equal(records1, records2):
    
    for i in range(len(records1['start'])):
        for j in range(3):
            if records1['start'][i][j] != records2['start'][i][j] or \
                records1['end'][i][j] != records2['end'][i][j]:
                return False
    return True
 
    
    
def verify_new_times(records, new_records):
    # If records and new_records are the same, then continue
    if check_records_equal(records, new_records):
        return True
    
    print('New quiz times are:')
    for i in range(len(new_records['start'])):
        print(f'''{i+1:2d}: {time_stamp_in_hms(*new_records['start'][i])} -- ''' +
             f'''{time_stamp_in_hms(*new_records['end'][i])}''')
    print()
    print('Old quiz times were:')
    for i in range(len(new_records['start'])):
        print(f'''{i+1:2d}: {time_stamp_in_hms(*records['start'][i])} -- ''' +
             f'''{time_stamp_in_hms(*records['end'][i])}''')
    confirm = input('Is this right? (y,n) [e to exit] ')
    if confirm.lower() == 'e':
        print('Exiting.')
        sys.exit(1)
    if confirm.lower() == 'y':
        return True
    return False

def write_to_file(new_records):
    head, filename = os.path.split(sys.argv[1])
    filename = f'updated_{filename}'
    with open(filename, 'w') as file:
        for i in range(len(new_records['start'])):
            file.write(f'{i+1};' + time_stamp_in_hms(*new_records['start'][i]) + ';' + 
                   time_stamp_in_hms(*new_records['end'][i]) + '\n')
    print(f'File written to {filename}.')    
    
def run():
    records = process_file()
    
    new_records = check_and_adjust_times(records)

    while not verify_new_times(records, new_records):
        new_records = check_and_adjust_times(records)

    write_to_file(new_records)
    return 0

if __name__ == '__main__':
    run()

