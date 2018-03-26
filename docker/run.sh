#!/bin/bash



IFS=
val="$(echo $1 | base64 -d )"

eval $val

exit

