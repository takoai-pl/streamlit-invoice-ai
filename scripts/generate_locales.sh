#!/bin/bash

# Function to generate .mo files and combine into base.po
generate_mo_files() {
    # Store the original directory
    original_dir=$(pwd)
    
    # Navigate to the locales directory
    cd locales

    # Loop over all language directories
    for lang_dir in */ ; do
        # Check if LC_MESSAGES directory exists
        if [ -d "$lang_dir/LC_MESSAGES" ]; then
            echo "Processing $lang_dir..."
            cd "$lang_dir/LC_MESSAGES"

            # Always generate .mo files for each domain
            for po_file in *.po; do
                if [ -f "$po_file" ] ; then
                    echo "  Generating .mo file for $po_file"
                    # Force regeneration of .mo file
                    msgfmt -o "${po_file%.po}.mo" "$po_file"
                fi
            done

            # Always create/overwrite base.po file with header
            cat > base.po << EOL
# Copyright (c) TaKo AI Sp. z o.o.

msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
EOL

            # Combine all .po files into base.po
            for po_file in *.po; do
                if [ -f "$po_file" ] && [ "$po_file" != "base.po" ]; then
                    echo "  Merging $po_file into base.po"
                    # Extract all msgid/msgstr pairs (excluding header) and append to base.po
                    awk 'BEGIN {p=0} /^msgid/ {if ($0 != "msgid \"\"") p=1} p==1 {print}' "$po_file" >> base.po
                    echo "" >> base.po  # Add newline between files
                fi
            done

            echo "  Generating base.mo from combined translations"
            # Force regeneration of base.mo
            msgfmt -o base.mo base.po

            # Go back to locales directory
            cd ../..
        else
            echo "Warning: LC_MESSAGES directory not found in $lang_dir"
        fi
    done

    # Return to the original directory
    cd "$original_dir"
}

# Function to check for differences between languages
check_translations() {
    # Store the original directory
    original_dir=$(pwd)
    
    # Navigate to the locales directory
    cd locales

    # Create a temporary file to store reference msgids
    ref_msgids=$(mktemp)
    ref_lang=""

    # Compare base.po across all language directories
    for lang_dir in */ ; do
        if [ -d "$lang_dir/LC_MESSAGES" ]; then
            target_file="$lang_dir/LC_MESSAGES/base.po"
            
            if [ -f "$target_file" ]; then
                # Extract msgids (excluding empty msgid)
                current_msgids=$(awk -F'"' '/msgid/ && !/^msgid ""/ {print $2}' "$target_file" | sort)

                # If this is our first language, use it as reference
                if [ -z "$ref_lang" ]; then
                    ref_lang="${lang_dir%/}"
                    echo "$current_msgids" > "$ref_msgids"
                else
                    # Compare with reference language
                    if ! diff -q <(echo "$current_msgids") "$ref_msgids" >/dev/null; then
                        echo "Warning: Translation differences found between $ref_lang and ${lang_dir%/}:"
                        echo "Missing in ${lang_dir%/}:"
                        diff <(echo "$current_msgids") "$ref_msgids" | grep "^>" || true
                        echo "Extra in ${lang_dir%/}:"
                        diff <(echo "$current_msgids") "$ref_msgids" | grep "^<" || true
                        echo
                    fi
                fi
            else
                echo "Warning: base.po not found in $lang_dir/LC_MESSAGES"
            fi
        fi
    done

    # Clean up
    rm "$ref_msgids"
    
    # Return to the original directory
    cd "$original_dir"
}

# Main execution
echo "Step 1: Generating individual .mo files and combining into base.mo..."
generate_mo_files

echo -e "\nStep 2: Checking translations..."
check_translations

echo -e "\nDone!"