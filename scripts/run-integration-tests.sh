# -*- coding: utf-8 -*-
#!/bin/sh

# causes the shell to exit if any subcommand or pipeline returns a non-zero status.
set -e

echo "Running Integration tests"

sleep 10s
python -m unittest discover -s ./ -p "*_itest.py";

echo "Done integration tests."