#!/bin/bash
list_of_times="$1"
video="$2"
video_filename="$(basename "$video")"
arg1_ext="$(echo $list_of_times | awk -F'.' '{print $NF}')"

if [[ "$#" -ne 2 ]];
then
	echo "Usage: ./cut_videos.sh list_of_times video"
	exit 1
fi

if !( echo "$arg1_ext" | grep -w "vtt" ) && !( echo "arg1_ext" | grep -w "txt" );
then
	echo "You passed $list_of_times as the first argument."
	echo "Ensure you have passed an (updated_)quiz_times_in_<transcript> as the first argument."
	exit 1
fi

while read p
do
	quiz_number=$(echo "$p" | awk -F';' '{print $1}')
	start_time=$(echo "$p" | awk -F';' '{print $2}')
	end_time=$(echo "$p" | awk -F';' '{print $3}')


	echo -e "Processing video $quiz_number from $start_time to $end_time\n"
	# echo ffmpeg -y -ss "$start_time" -to "$end_time" -i "$video" -c copy quiz_"$quiz_number"_"$start_time"_"$end_time"_"$video" -nostdin
	ffmpeg -y -ss "$start_time" -to "$end_time" -i "$video" -c copy quiz_"$quiz_number"_"$start_time"_"$end_time"_"$video_filename" -nostdin
done < "$list_of_times"

echo -e "Done.\n"
