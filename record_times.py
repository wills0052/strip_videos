# This script creates a file named quizzes_yyyy_mm_dd
# that inputs a time stamp each time it is run
# in a separate row


from datetime import datetime
date_and_time = datetime.now()
# day_of_week is 0 for Mon, 6 for Sun
day_of_week = date_and_time.weekday()
# 
time_stamp = [int(i) for i in date_and_time.strftime('%H:%M:%S').split(':')]


def minutes_and_seconds_to_seconds(minutes, seconds):
    return minutes * 60 + seconds

def seconds_to_minutes_and_seconds(seconds):
    return divmod(seconds, 60)

# If lecture starts on the hour, starts_at_minute = 0
# If lecture starts at 15 mins past the hour, starts_at_minute = 15
# length_of_introduction is the length of the university copyright
#   in seconds
# Only works for less than 1 hour long
# returns in seconds the difference between current time and starts_at_minute
#   accounting for the intro
def time_delta_in_seconds(starts_at_minute, length_of_introduction):
    if day_of_week == 0:
        start_time = list(time_stamp) #[HH, MM, SS] in integers
        
        # If current minutes is between 00 and 05, subtract one from hour
        # If current minutes is between 00 and 20, subtract 1 from hour
        if start_time[1] <= starts_at_minute + 5:
            start_time[0] = start_time[0] - 1
        start_time[1] = starts_at_minute
        start_time[2] = 0
        
        joined_start_time = ':'.join(str(i) for i in start_time)
        joined_current_time = ':'.join(str(i) for i in time_stamp)
        time_delta = datetime.strptime(joined_current_time, '%H:%M:%S') \
                        - datetime.strptime(joined_start_time, '%H:%M:%S')
        
        return time_delta.seconds - length_of_introduction

# Need hours for ffmpeg
def time_stamp_in_hh_mm_ss(minutes, seconds):
    return f'00:{minutes:02d}:{seconds:02d}'

def run():
    # Edit which minute lecture starts
    if day_of_week == 0:
        starts_at_minute = 0
    else:
        starts_at_minute = 15

    with open(f'quizzes_{date_and_time.strftime("%Y_%m_%d")}.txt', 'a') as file:
        minutes, seconds = seconds_to_minutes_and_seconds(time_delta_in_seconds( \
        # Change length of introduction here
                            starts_at_minute, length_of_introduction = 14))
        minutes, seconds = max(minutes, 0), max(seconds, 0)
        file.write(time_stamp_in_hh_mm_ss(minutes, seconds) + '\n')
               
if __name__ == "__main__":
    run()
