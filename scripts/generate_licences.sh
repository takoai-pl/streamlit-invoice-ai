#!/bin/bash

# Define the license text
LICENSE_TEXT='# Copyright (c) TaKo AI Sp. z o.o.

'

# Function to prepend the license text to a file
prepend_license() {
    # Check if the license text already exists in the file
    if ! grep -q "Copyright (c) TaKo AI Sp. z o.o." $1; then
        echo "$LICENSE_TEXT$(cat $1)" > $1
    fi
}

# Find all .py files in the tests/ and src/ directories and prepend the license text
for file in $(find tests/ src/ -name '*.py'); do
    prepend_license $file
done