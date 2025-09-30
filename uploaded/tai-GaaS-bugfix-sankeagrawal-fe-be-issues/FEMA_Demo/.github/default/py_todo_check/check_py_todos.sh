#!/bin/sh -l

# default passed is true, if fails checks then passed is false
passed=1


todos=$(egrep --include="*.py" -rn "\bXXX\b|fillme|FILLME|\bxxx\b|TODO|todo|to-do|FIXME|fix-me|fixme|fix me|FIX ME|TO DO" *)
case $? in
    0) echo $todos && passed=0;;
    *) echo "No TODO's found";;
esac

case $passed in
    0) exit 1;;
    1) exit 0;;
esac