# strip_videos
The following contains three scripts that may be used to automate cutting segments out of videos based on timestamps in transcripts.

# Dependencies
For python, we use ```collections, os, sys, re```. We also require ```ffmpeg```
# Usage
## Extract quiz start times from transcript
Provided a Zoom transcript file, 
```
python3 find_quiz_times.py <transcriptfile>
```
will output a file called ```<quiz_times_in_transcriptfile>``` which contains quiz start and end times and will flag any unbalanced start/end times which can be edited in the transcript manually.

## Adjust times by a fixed time offset
Provided a file output by ```find_quiz_times.py```, 
```
python3 offset_times.py <quiz_times_in_transcriptfile>
```
will provide an interactive program in the terminal. It lists the start time of the first quiz and allows the user to specify the new start time in ```hh:mm:ss```. It will prompt for user confirmation and output a file ```updated_quiz_times_in_transcriptfile``` which contains the new times.

## Cut segments of video
Provided either the original ```<quiz_times_in_transcriptfile>``` or ```<updated_quiz_times_in_transcriptfile>```,
```
./cut_videos.sh <(updated_)quiz_times_in_transcriptfile> <video>
```
will cut the desired segments and output them as ```quiz_<number>_<start_time>_<end_time>_video```.
