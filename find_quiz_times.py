import sys, os, re
from collections import defaultdict
from itertools import product
from pathlib import Path

start_list = ['start', 'starts', 'started', 'begin', 'begins']
end_list = ['stop', 'stops', 'stopped', 'end', 'ends', 'ended']

start_phrases = [' '.join(i) for i in product(['quiz'], start_list)] + \
            [' '.join(i) for i in product(start_list, ['quiz'])]

end_phrases = [' '.join(i) for i in product(['quiz'], end_list)] + \
            [' '.join(i) for i in product(end_list, ['quiz'])]
key_words = ['explanation', 'slide', 'start']
optional_key_words = ['poll', 'quiz', 'question']

def phrase_in_string(list_of_phrases, string):
    return any(i for i in list_of_phrases if i in string)
def all_phrases_in_string(list_of_phrases, string):
    for i in list_of_phrases:
        if i not in string:
            return False
    return True

def scrape_times(file_location):
    time_stamps = defaultdict(list)

    with open(file_location) as file:
        for line in file:
            if '-->' in line:
                split_times = line.split()
                start_time, end_time = split_times[0][:8], split_times[2][:8]
            lowercase_line = line.lower()
            # Should always have time_stamps['start'] and time_stamps['end']
            # the same length before adding new one
            # Put a mark if there is a problem
            if ('quiz' in lowercase_line and 
                phrase_in_string(start_phrases, lowercase_line)) or \
                (phrase_in_string(optional_key_words, lowercase_line) and \
                all_phrases_in_string(key_words, lowercase_line)):
                if len(time_stamps['start']) != len(time_stamps['end']):
                    time_stamps['end'].append(start_time + '*')
                time_stamps['start'].append(start_time)
            
            # Time_stamps['start'] should always be one more than time_stamps['end']
            elif 'quiz' in lowercase_line and phrase_in_string(end_phrases, lowercase_line):
                if len(time_stamps['end']) == len(time_stamps['start']):
                    time_stamps['start'].append(start_time + '*')
                time_stamps['end'].append(end_time)
        
        # Add last time-stamp if missing
        if len(time_stamps['start']) != len(time_stamps['end']):
            time_stamps['end'].append(end_time + '*')

    return time_stamps
                
def pair_times(file_location, time_stamps):
    print('The times are:')
    new_file_location = file_location.parent / f'quiz_times_in_{file_location.name}'
    
    with open(new_file_location, 'w') as file:
        for i in range(len(time_stamps['start'])):
            check = ''
            if '*' in time_stamps['start'][i]:
                check = 'check_start'
                time_stamps['start'][i] = time_stamps['start'][i][:-1]
            elif '*' in time_stamps['end'][i]:
                check = 'check_end'
                time_stamps['end'][i] = time_stamps['end'][i][:-1]
            else:
                check = ' '
            string = f'{i+1:2d};' + time_stamps['start'][i] \
                           + ';' + time_stamps['end'][i] + f';{check}\n'
            
            print(f'''{i+1:2d}: {time_stamps['start'][i]} -- ''' + 
                  f'''{time_stamps['end'][i]} {check}''')
            
            file.write(string)
    print(f'File written to {new_file_location}')


def run(transcript):
    file = Path(transcript)
    time_stamps = scrape_times(file)
    if len(time_stamps['start']) == 0:
        print('No time stamps detected. Exiting')
        sys.exit(1)
    pair_times(file, time_stamps)
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 find_quiz_times.py transcript.vtt')
        sys.exit(1)    
    run(sys.argv[1])
