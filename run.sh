#!/bin/bash
transcript="$1"
video="$2"
arg1_ext="$(echo $transcript | awk -F'.' '{print $NF}')"
filename="$(basename "$transcript")"

cut_videos () {
	echo -e "Cutting video.\n"
	./cut_videos.sh "updated_quiz_times_in_$filename" "$video"
}

offset_times () {
	echo -e "Checking quiz times in "$filename".\n"
	python3 offset_times.py "quiz_times_in_$filename"
}

find_times () {
	echo -e "Finding quiz times in "$transcript".\n"
	python3 find_quiz_times.py "$transcript"

}


if [[ "$#" -ne 2 ]]
then
	echo "Usage: ./run.sh <transcript> <video>"
	exit 1
fi

if !( echo "$arg1_ext" | grep -w "vtt" )
then
	echo "You passed $transcript as the first argument."
	echo "Ensure you have passed a zoom .vtt transcript as the first argument."
	exit 1
fi

echo 

find_times && (offset_times && cut_videos || exit 1) || exit 1

echo -e "Done."
