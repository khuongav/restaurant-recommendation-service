set -e

echo "Running unit tests"

echo "Start running unit tests ..."
find . -type f -name *_test.py  |
while read filename
do
    echo 'Testing for: ' $(basename "$filename")
    python3 -m unittest discover -s ./ -p $(basename "$filename")
done
echo "Done unit tests."

./scripts/run-coverage.sh