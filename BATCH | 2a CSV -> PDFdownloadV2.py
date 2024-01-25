import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, unquote  # Import unquote
import os


def is_pdf(url):
    # Check if the URL ends with '.pdf'
    return url.lower().endswith('.pdf')

def download_pdf(url, download_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Extract the filename from the URL
        filename = os.path.join(download_path, os.path.basename(urlparse(url).path))

        # Save the PDF file
        with open(filename, 'wb') as file:
            file.write(response.content)

        return True, f"Downloaded: {filename}"

    except requests.exceptions.RequestException as e:
        return False, f"Error downloading {url}: {e}"

def process_csv_file(file_path, download_path):
    with open(file_path, 'r') as file:
        for line in file:
            link = line.strip()

            # Skip empty entries and entries that are not links
            if not link or not link.startswith('http'):
                continue

            # Decode URL if needed
            decoded_link = unquote(link)

            # Skip links that are not PDFs
            if not is_pdf(decoded_link):
                continue

            success, message = download_pdf(decoded_link, download_path)
            print(message)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def browse_directory():
    download_path = filedialog.askdirectory()
    entry_download_path.delete(0, tk.END)
    entry_download_path.insert(0, download_path)

def start_download():
    file_path = entry_file_path.get()
    download_path = entry_download_path.get()

    if not file_path or not download_path:
        result_label.config(text="Please select CSV file and download directory.")
        return

    process_csv_file(file_path, download_path)
    result_label.config(text="Download completed!")

# Create the main window
window = tk.Tk()
window.title("PDF Downloader")

# Create and place widgets
label_file_path = tk.Label(window, text="CSV File:")
label_file_path.grid(row=0, column=0, padx=10, pady=10)

entry_file_path = tk.Entry(window, width=50)
entry_file_path.grid(row=0, column=1, padx=10, pady=10)

button_browse_file = tk.Button(window, text="Browse", command=browse_file)
button_browse_file.grid(row=0, column=2, padx=10, pady=10)

label_download_path = tk.Label(window, text="Download Directory:")
label_download_path.grid(row=1, column=0, padx=10, pady=10)

entry_download_path = tk.Entry(window, width=50)
entry_download_path.grid(row=1, column=1, padx=10, pady=10)

button_browse_directory = tk.Button(window, text="Browse", command=browse_directory)
button_browse_directory.grid(row=1, column=2, padx=10, pady=10)

button_start_download = tk.Button(window, text="Start Download", command=start_download)
button_start_download.grid(row=2, column=1, pady=20)

result_label = tk.Label(window, text="")
result_label.grid(row=3, column=1)

# Run the GUI
window.mainloop()
