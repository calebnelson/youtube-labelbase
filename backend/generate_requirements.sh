#!/bin/bash

# Generate requirements.txt from Pipfile
pipenv requirements > requirements.txt

# Remove any dev dependencies
sed -i '' '/^pytest/d' requirements.txt
sed -i '' '/^black/d' requirements.txt
sed -i '' '/^isort/d' requirements.txt
sed -i '' '/^flake8/d' requirements.txt

echo "Generated requirements.txt from Pipfile" 