import csv
import os
import re
import pdfkit
from tkinter import Tk, filedialog

# Function to clean illegal characters from filenames
def clean_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)

# Create the Tkinter root window (it will be hidden)
root = Tk()
root.withdraw()

# Ask the user to select the CSV file
csv_file_path = filedialog.askopenfilename(
    title="Select CSV File",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)

# Check if the user selected a file
if not csv_file_path:
    print("No CSV file selected. Exiting.")
    exit()

# Path to the downloads folder
downloads_folder = os.path.expanduser('~/Downloads')

# Create a folder for PDFs if it doesn't exist
pdf_folder = os.path.join(downloads_folder, 'pdf')
os.makedirs(pdf_folder, exist_ok=True)

# Read URLs from CSV
with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    urls = [row[0] for row in reader]

# Iterate through the URLs and save PDFs
for url in urls:
    # Get the page title for the PDF filename
    title = url.split('//')[-1].replace('/', '_')
    clean_title = clean_filename(title)

    # Set the PDF filename
    pdf_filename = f'{clean_title}.pdf'
    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # Use pdfkit to save the webpage as a PDF with images
    options = {
        'quiet': '',
        'no-images': False
    }
    pdfkit.from_url(url, pdf_path, options=options)

print("PDFs saved successfully.")

