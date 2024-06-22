#!/bin/bash

# Function to check for differences
check_diffs() {
    # Navigate to the locales directory
    cd locales

    # Create a temporary file to store the msgids of the first base.po file
    first_file_msgids=$(mktemp)

    # Loop over all subdirectories
    for lang_dir in */ ; do
        # Check if LC_MESSAGES directory exists for the current language
        if [ -d "$lang_dir/LC_MESSAGES" ]; then
            # Navigate to the LC_MESSAGES directory for the current language
            cd "$lang_dir/LC_MESSAGES"

            # Check if base.po file exists
            if [ -f "base.po" ]; then
                # Run msgfmt on the base.po file
                msgfmt base.po -o base.mo

                # Extract msgids from the base.po file
                msgids=$(awk -F'"' '/msgid/ {print $2}' base.po)

                # If first_file_msgids is empty, store the msgids of the first file
                if [ -z "$(cat $first_file_msgids)" ]; then
                    echo "$msgids" > $first_file_msgids
                else
                    # Compare the msgids with the first file
                    diff_msgids=$(diff <(echo "$msgids") $first_file_msgids)

                    # If there are differences, log them and return with error status
                    if [ -n "$diff_msgids" ]; then
                        echo "Differences in msgids found in $lang_dir/LC_MESSAGES/base.po:"
                        echo "$diff_msgids"
                        echo "Error: Differences in locales keys found. Please resolve the differences before proceeding."
                        return 1
                    fi
                fi
            else
                echo "base.po file not found in $lang_dir/LC_MESSAGES"
            fi

            # Navigate back to the locales directory
            cd - > /dev/null
        else
            echo "LC_MESSAGES directory not found in $lang_dir"
        fi
    done

    # Remove the temporary file
    rm $first_file_msgids
}

# Call the function and exit with its status
check_diffs
exit $?