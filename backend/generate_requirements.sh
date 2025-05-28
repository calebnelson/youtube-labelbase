#!/bin/bash

# Generate requirements.txt from Pipfile into app directory
pipenv requirements > app/requirements.txt

# Remove any dev dependencies
sed -i '' '/^pytest/d' app/requirements.txt
sed -i '' '/^black/d' app/requirements.txt
sed -i '' '/^isort/d' app/requirements.txt
sed -i '' '/^flake8/d' app/requirements.txt

# Remove version constraints and keep only the package names
sed -i '' 's/;.*$//' app/requirements.txt
sed -i '' 's/==.*$//' app/requirements.txt

# Remove the -i line
sed -i '' '/^-i/d' app/requirements.txt

# Remove empty lines
sed -i '' '/^$/d' app/requirements.txt

echo "Generated simplified requirements.txt in app directory from Pipfile" 