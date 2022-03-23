# strip_videos
This contains four scripts that may be used to automate cutting segments out of videos based on timestamps of keywords in transcripts.

# Dependencies
For python, we use ```collections, os, sys, re, itertools```. We also require ```ffmpeg```.

# Usage
## Bookmarking quiz times
The script looks for occurrences of "quiz start(s/ed)", "quiz stop(s/ed)" in the Zoom transcript. These can be added in manually after the fact.

## Extract quiz start times from transcript
Provided a Zoom transcript file in the working directory,
```
python3 find_quiz_times.py <transcriptfile.vtt>
```
will output a file called ```<quiz_times_in_transcriptfile.vtt>``` which contains quiz start and end times and will flag any unbalanced start/end times which can be edited in the transcript manually. 

## Adjust times by a fixed time offset
Provided a file output by ```find_quiz_times.py``` with ```.vtt``` extension, 
```
python3 offset_times.py <quiz_times_in_transcriptfile.vtt>
```
will provide an interactive program in the terminal. It lists the start time of the first quiz and allows the user to confirm or specify the new start time in ```hh:mm:ss```. It will prompt for user confirmation and output a file ```<quiz_times_in_transcriptfile>``` which contains the new times. It will replace the file.

## Cut segments of video
Privided with the <quiz_times_in_transcriptfile.vtt> file,
```
./cut_videos.sh <quiz_times_in_transcriptfile.vtt> <video>
```
will cut the desired segments and output them as ```quiz_<number>_<start_time>_<end_time>_video```. It will output video clips to the same directory that <video> is in.

## Run all three above in one go
Provided a zoom ```.vtt``` transcript file and a video, 
```
./run.sh <transcript.vtt> <video>
```
will extract quiz times. It will then run the second script to ask for adjustments. Finally it will cut the segments out and output them to the current directory.
