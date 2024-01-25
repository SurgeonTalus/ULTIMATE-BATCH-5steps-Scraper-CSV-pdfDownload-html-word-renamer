import csv
import os
import re
import pdfkit
from tkinter import Tk, filedialog
import requests

# Function to clean illegal characters from filenames
def clean_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)

# Function to download a file given a URL
def download_file(url, pdf_folder, office_folder, other_folder):
    try:
        # Get the page title for the filename
        title = url.split('//')[-1].replace('/', '_')
        clean_title = clean_filename(title)

        # Set the filename
        filename = f'{clean_title}.pdf' if url.lower().endswith('.pdf') else f'{clean_title}'

        # Check for specific file types
        if url.lower().endswith(('.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls')):
            file_path = os.path.join(office_folder, f'{filename}.zip')
        elif "docs.google.com" in url:
            if "/document/" in url:
                file_path = os.path.join(office_folder, f'{filename}.gdoc')
            elif "/spreadsheets/" in url:
                file_path = os.path.join(office_folder, f'{filename}.gsheet')
            elif "/presentation/" in url:
                file_path = os.path.join(office_folder, f'{filename}.gslides')
            else:
                file_path = os.path.join(other_folder, filename)
        else:
            file_path = os.path.join(pdf_folder, filename)

        # Download the file content
        response = requests.get(url)
        response.raise_for_status()

        # Save the content to the file
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"File saved successfully: {file_path}")

    except Exception as e:
        print(f"Error downloading file from {url}: {str(e)}")

# Create the Tkinter root window (it will be hidden)
root = Tk()
root.withdraw()

# Ask the user to select the destination folder
destination_folder = filedialog.askdirectory(title="Select Destination Folder")

# Check if the user selected a folder
if not destination_folder:
    print("No destination folder selected. Exiting.")
    exit()

# Read URLs from CSV
csv_file_path = filedialog.askopenfilename(
    title="Select CSV File",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)

# Check if the user selected a file
if not csv_file_path:
    print("No CSV file selected. Exiting.")
    exit()

# Create folders for PDFs, office files, and other files in the destination folder
pdf_folder = os.path.join(destination_folder, 'Pfiles')
office_folder = os.path.join(destination_folder, 'office')
other_folder = os.path.join(destination_folder, 'other')
os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(office_folder, exist_ok=True)
os.makedirs(other_folder, exist_ok=True)

# Iterate through the URLs and save files
with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    urls = [row[0] for row in reader]

# Iterate through the URLs and save files
for url in urls:
    # Download the file based on its type
    download_file(url, pdf_folder, office_folder, other_folder)

print("Processing completed.")
