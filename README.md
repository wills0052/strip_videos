# strip_videos
This contains four scripts that may be used to automate cutting segments out of videos based on timestamps of keywords in transcripts.

# Dependencies
For python, we use ```collections, os, sys, re, itertools, ffmpeg, and pathlib```. We also require ```ffmpeg``` to be installed an in the PATH environment. After the latest update there is no need for any bash.

# Usage
## Bookmarking quiz times
The script looks for either 1) occurrences of all the words ["explanation", "slide" and "start(s/ed)"], and one of the words ["poll", "quiz", "question"]; or 2) "quiz start(s/ed)" in a line to mark the start of the expalnation. It also looks for "quiz stop(s/ed)" (subject to change) in the Zoom transcript but this is optional. These can be added in manually after the fact.

## Running all scripts at once
Provided a zoom ```.vtt``` transcript file and a video, 
```
python3 run.py <transcript.vtt> <video>
```
or in Bash (may be deprecated soon)
```
./run.sh <transcript.vtt> <video>
```
will extract quiz times. It will then run the second script to ask for adjustments. Finally it will cut the segments out and output them to the current directory.

## Extract quiz start times from transcript
Provided a Zoom transcript file,
```
python3 find_quiz_times.py <transcript.vtt>
```
will output a file called ```<quiz_times_in_transcript.vtt>``` in the same directory as the transcript. The filw contains quiz start and end times and will flag any unbalanced start/end times which can be edited in the transcript manually. 

## Adjust times by a fixed time offset
Provided a file output by ```find_quiz_times.py``` with ```.vtt``` extension, 
```
python3 offset_times.py <quiz_times_in_transcript.vtt>
```
will provide an interactive program in the terminal. It lists the start time of the first quiz and allows the user to confirm or specify the new start time in ```hh:mm:ss```. It will prompt for user confirmation and output a file ```<quiz_times_in_transcriptfile>``` which contains the new times. It also produces a warning if start times are over 5 minutes long, and provides an option to reduce the maximum video length. It will replace the file.

## Cut segments of video
Privided with the <quiz_times_in_transcript.vtt> file,
```
python3 cut_videos.py <quiz_times_in_transcript.vtt> <video>
```
or in bash (may be deprecated soon)
```
./cut_videos.sh <quiz_times_in_transcript.vtt> <video>
```
will cut the desired segments and output them as ```quiz_<number>_video```. It will output video clips to the same directory that <video> is in.


