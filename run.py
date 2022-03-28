import offset_times, cut_videos, find_quiz_times
import os, sys
from pathlib import Path

def run():
    if len(sys.argv) != 3 or sys.argv[1][-3:] != 'vtt':
        print('Usage: python3 transcript.vtt video')
        sys.exit(1)
    transcript_location = Path(sys.argv[1])
    quiz_times_location = transcript_location.parent / f'quiz_times_in_{transcript_location.name}'
    video_location = Path(sys.argv[2])
    
    print(f'Finding quiz times in {transcript_location}')
    find_quiz_times.run(transcript_location)
    print()
    
    print(f'Checking quiz times in {quiz_times_location}')
    offset_times.run(quiz_times_location)
    print()
    
    print(f'Extracing quizzes from {video_location}')
    cut_videos.run(quiz_times_location, video_location)
    print()
    
    print('Done.')
    return 0
    
if __name__ == '__main__':
    run()
    
    
    
