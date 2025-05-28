#!/bin/bash

# Generate requirements.txt from Pipfile
pipenv requirements > requirements.txt

# Remove any dev dependencies
sed -i '' '/^pytest/d' requirements.txt
sed -i '' '/^black/d' requirements.txt
sed -i '' '/^isort/d' requirements.txt
sed -i '' '/^flake8/d' requirements.txt

# Remove version constraints and keep only the package names
sed -i '' 's/;.*$//' requirements.txt
sed -i '' 's/==.*$//' requirements.txt

# Remove the -i line
sed -i '' '/^-i/d' requirements.txt

# Remove empty lines
sed -i '' '/^$/d' requirements.txt

echo "Generated simplified requirements.txt from Pipfile" 