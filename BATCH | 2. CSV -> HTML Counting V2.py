import tkinter as tk
from tkinter import filedialog
import csv
import re
import subprocess
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from readability import Document
import appscript
import mactypes

# Counter for cumulative counting
file_counter = 1

def generate_filename(url):
    global file_counter
    parsed_url = urlparse(url)
    fragments = parsed_url.fragment or None
    subdirectory = parsed_url.path.split('/')[1] if len(parsed_url.path.split('/')) > 1 else 'no-subdirectory'
    second_level_domain = parsed_url.netloc.split('.')[-2] if len(parsed_url.netloc.split('.')) > 1 else 'no-second-level-domain'
    top_level_domain = parsed_url.netloc.split('.')[-1] if len(parsed_url.netloc.split('.')) > 0 else 'no-top-level-domain'

    if not fragments:
        fragments = parsed_url.path.split('/')[2] if len(parsed_url.path.split('/')) > 2 else 'no-fragment'

    # Replace hyphens in fragments with spaces
    fragments = fragments.replace('-', ' ')

    filename = f"{subdirectory}-{fragments}-{second_level_domain}.{top_level_domain}-{file_counter}"
    filename = re.sub(r'[^\w\s.-]', '', filename)
    file_counter += 1
    return filename

def extract_main_content(html_content):
    doc = Document(html_content)
    main_content = doc.summary(html_partial=True)
    return main_content

def extract_styles(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    style_elements = soup.find_all('style')
    return '\n'.join([str(style) for style in style_elements])

def extract_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    image_elements = soup.find_all('img')
    return '\n'.join([str(img) for img in image_elements])

def save_html(url, save_path):
    global file_counter
    filename = generate_filename(url)
    command = f'docker run --rm -v {os.path.abspath(save_path)}:/output singlefile {url}'

    try:
        html_content = subprocess.check_output(command, shell=True, text=True)

        # Extract main article content
        main_content = extract_main_content(html_content)

        # Extract styles
        styles = extract_styles(html_content)

        # Extract images
        images = extract_images(html_content)

        filepath = f'{filename}.html'

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(f"<html><head>{styles}</head><body>{main_content}{images}</body></html>")

        # Add webpage URL to comments using appscript
        file_alias = mactypes.Alias(os.path.abspath(filepath))
        file = appscript.app('Finder').items[file_alias]
        file.comment.set(f"Website: {url}")

    except subprocess.CalledProcessError as e:
        print(f"Error processing URL {url}: {e}")
        pass  # Skip to the next link

def process_csv(csv_file, save_path):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            url = row[0]
            save_html(url, save_path)

def browse_file():
    global file_counter
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        save_path = filedialog.askdirectory(initialdir="~/Downloads")
        if save_path:
            os.chdir(save_path)
            file_counter = 1  # Reset counter for each new operation
            process_csv(file_path, save_path)
            status_label.config(text="HTML files saved successfully.")
        else:
            status_label.config(text="Operation canceled.")
    else:
        status_label.config(text="Operation canceled.")

# Create the main window
root = tk.Tk()
root.title("URL to HTML Converter")

# Create and pack widgets
browse_button = tk.Button(root, text="Browse CSV File", command=browse_file)
browse_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Run the main loop
root.mainloop()
