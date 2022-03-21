# This file processes a given quizzes_yyyy_mm_dd.txt file
# and creates a new quizzes_yyyy_mm_dd-collated.txt file
# in which each row is quiz_number;start_time;end_time
# to be processed by a bash script to split the mp4 files

import sys
records = []


def minutes_and_seconds_to_seconds(minutes, seconds):
    return minutes * 60 + seconds

def seconds_to_minutes_and_seconds(seconds):
    return divmod(seconds, 60)
def time_stamp_in_hh_mm_ss(minutes, seconds):
    return f'00:{minutes:02d}:{seconds:02d}'

def check_and_adjust_times():
    new_records = []
    start_ok = input(f'Does the first quiz start at {records[0][0]}:{records[0][1]}? (y,n) ')
    if start_ok.lower() == 'n':
        new_start_input = input(f'What is the correct start time? (mm:ss) ')
        new_start_time = tuple(int(i) for i in new_start_input.replace('\n', '').split(':'))
        new_start_time_in_seconds = minutes_and_seconds_to_seconds(*new_start_time)
        old_start_time_in_seconds = minutes_and_seconds_to_seconds(*records[0])
        
        offset = new_start_time_in_seconds - old_start_time_in_seconds
        
        for i in records:
            new_time_in_seconds = max(minutes_and_seconds_to_seconds(*i) + offset, 0)
            new_time_in_minutes_seconds = seconds_to_minutes_and_seconds(new_time_in_seconds)
            new_records.append(new_time_in_minutes_seconds)
            
    else:
        new_records = list(records)
    return new_records


    
def run():
    if len(sys.argv) != 2:
        print('Usage: python3 collate_times.py file.txt')
        sys.exit(1)
    with open(str(sys.argv[1])) as file:
        for line in file:
            print(line, end='')
            records.append(tuple(int(i) for i in line.replace('\n', '').split(':')[1:]))
        if len(records) % 2:
            print('There is an odd number of quiz times.' +
                  'Please check the times.')
            sys.exit(1)
    new_records = check_and_adjust_times()
    
    print('The new times are:')
    for i in new_records:
        print(f'{time_stamp_in_hh_mm_ss(*i)}')
    confirm = input('Is this right? (y,n) ')
    if confirm.lower() == 'y':
        with open(f'collated_{sys.argv[1]}', 'w') as file:
            for i in range(len(new_records) // 2):
                file.write(f'{i+1};' + time_stamp_in_hh_mm_ss(*new_records[2*i]) + ';' + 
                       time_stamp_in_hh_mm_ss(*new_records[2*i+1]) + '\n')
        

if __name__ == '__main__':
    run()
    
    
