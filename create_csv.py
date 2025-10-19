import pyperclip
import csv
import re
import sys
import os

def sanitize_filename(filename):
    """
    Removes characters that are not allowed in filenames on most systems.
    """
    # Remove characters that are invalid in Windows, macOS, and Linux filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def create_csv_from_clipboard():
    """
    Creates a CSV file from the content of the clipboard inside a 'CSV Files' folder.

    The first line of the clipboard content is used as the filename,
    and the subsequent lines are written as rows to the CSV file.
    """
    try:
        # Define the output folder
        output_folder = "CSV Files"
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Step 1: Get content from the system clipboard
        clipboard_content = pyperclip.paste()

        if not clipboard_content or not clipboard_content.strip():
            print("Clipboard is empty. Please copy some text first.")
            return

        # Step 2: Split the content into individual lines
        lines = clipboard_content.strip().splitlines()

        if len(lines) < 2:
            print("Error: Not enough content on the clipboard.")
            print("You need at least two lines: one for the filename and one for the data.")
            return

        # Step 3: Sanitize the first line to create a valid filename
        filename_base = sanitize_filename(lines[0])
        if not filename_base:
            print("Error: The first line is not a valid base for a filename.")
            return
        
        # Construct the full path for the new CSV file
        filename_csv = f"{filename_base}.csv"
        full_path = os.path.join(output_folder, filename_csv)

        # Step 4: Get the remaining lines which will be the CSV data
        csv_data_lines = lines[1:]

        # Step 5: Write the data to the new CSV file
        with open(full_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Use csv.reader to properly interpret the lines from the clipboard.
            # This handles cases where your data might have commas inside quotes.
            csv_writer = csv.writer(csvfile)
            reader = csv.reader(csv_data_lines)
            
            # Write each parsed row to the new file
            for row in reader:
                csv_writer.writerow(row)

        print(f"Successfully created CSV file: '{full_path}'")

    except pyperclip.PyperclipException:
        print("Error: Pyperclip could not access the clipboard.", file=sys.stderr)
        print("On Linux, you may need to install 'xclip' or 'xsel'.", file=sys.stderr)
        print("Try: sudo apt-get install xclip", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    create_csv_from_clipboard()

