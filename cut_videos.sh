#!/bin/bash
list_of_times="$1"
video="$2"

while read p
do
	quiz_number=$(echo "$p" | awk -F';' '{print $1}')
	start_time=$(echo "$p" | awk -F';' '{print $2}')
	end_time=$(echo "$p" | awk -F';' '{print $3}')

	echo "Processing video $quiz_number from $start_time to $end_time"
	#echo "ffmpeg -ss $start_time -i "$video" -to $end_time -c copy quiz_"$quiz_number"_"$start_time"_"$end_time"_"$video""
	ffmpeg -y -ss "$start_time" -to "$end_time" -i "$video" -c copy quiz_"$quiz_number"_"$start_time"_"$end_time"_"$video" -nostdin
done < "$list_of_times"

echo "Done."
