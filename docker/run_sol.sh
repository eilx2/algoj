#!/bin/bash



IFS=

input=`cat`
echo "$1" > sol.py
echo "$input" > input.txt

timeout  -s SIGKILL $2 python3 sol.py < input.txt > out.txt
echo $?
if [ $? -eq 0 ]
then
	cat out.txt
else
	exit $?
fi

exit

