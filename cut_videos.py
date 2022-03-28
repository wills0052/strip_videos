import ffmpeg, sys, os
from pathlib import Path
from collections import defaultdict

def process_file(transcript):
    records = defaultdict(list)
    if os.stat(transcript).st_size == 0:
        print('No times detected.')
        sys.exit(1)

    with open(transcript) as file:
        for line in file:
            try:
                quiz_number, start_time, end_time, _ = line.split(';')
                records['start'].append(start_time)
                records['end'].append(end_time)
            except ValueError:
                print('Invalid input file. Check it has been processed by find_quiz_times.py and is of the form #;hh:mm:ss;hh:mm:ss; \n')
                sys.exit(1)
                
    return records

def cut_video(original_video, records):
    original_video_name = original_video.name
    for i in range(len(records['start'])):
        print(f'''Processing video {i+1} from {records['start'][i]}--{records['end'][i]}''')
        video_clip = ffmpeg.input(original_video, 
                                  ss=records['start'][i],
                                  to=records['end'][i])
        new_video_name = original_video.parent / f'quiz_{i+1}_{original_video_name}'
        print(new_video_name)
        output = ffmpeg.output(video_clip, f'{new_video_name}', vcodec='copy', acodec='copy')
        ffmpeg.overwrite_output(output).run()

    print('Done')
    
def run(transcript, video):

    records = process_file(Path(transcript))
    cut_video(Path(video), records)
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 3 or transcript[-3:] != 'vtt':
        print('Usage: python3 quiz_times_in_transcript.vtt video')
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])
