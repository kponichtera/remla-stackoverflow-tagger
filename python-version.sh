ver=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -gt "39" ] || [ "$ver" -lt "36" ]; then
    echo "This script requires python >=3.6 and <=3.9";
    exit 1;
fi
