import sys, os
from collections import defaultdict

start_phrases = {'start', 'starts', 'started', 'begin', 'begins'}
end_phrases = {'stop', 'stops', 'stopped', 'end', 'ends', 'ended'}

def phrase_in_string(list_of_phrases, string):
    return any(i for i in list_of_phrases if i in string)

def scrape_times(file_string):
    time_stamps = defaultdict(list)
    if len(sys.argv) != 2:
        print('Usage: python3 find_quiz_times.py transcript.vtt')
        sys.exit(1)
    with open(file_string) as file:
        for line in file:
            if '-->' in line:
                split_times = line.split()
                start_time, end_time = split_times[0][:8], split_times[2][:8]
            lowercase_line = line.lower()
            # Should always have time_stamps['start'] and time_stamps['end']
            # the same length before adding new one
            # Put a mark if there is a problem
            elif 'quiz' in lowercase_line and phrase_in_string(start_phrases, lowercase_line):
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
                
def pair_times(file_string, time_stamps):
    print('The times are:')
    path, filename = os.path.split(file_string)
    filename = f'{path}/quiz_times_in_{filename}'
    with open(filename, 'w') as file:
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
    print(f'File written to {filename}')


def run():
    file_string = str(sys.argv[1])
    time_stamps = scrape_times(file_string)
    if len(time_stamps['start']) == 0:
        print('No time stamps detected. Exiting')
        sys.exit(1)
    pair_times(file_string, time_stamps)
    
if __name__ == '__main__':
    run()
