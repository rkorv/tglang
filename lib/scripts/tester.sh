#!/bin/bash
cd "$(dirname "$0")"

BASE_DIR=/data/dataset

TIMEFORMAT=%R
echo "time,prediction,file"

find "$BASE_DIR" -type f | while read -r file; do
    RETURN_VALUE=$( { time /app/build/libtglang-tester/libtglang-tester "$file" ; } 2>&1 )
    PREDICTION=$(echo "$RETURN_VALUE" | head -n -1)
    EXEC_TIME=$(echo "$RETURN_VALUE" | tail -n 1)
    echo "$EXEC_TIME,$PREDICTION,$file"
done
