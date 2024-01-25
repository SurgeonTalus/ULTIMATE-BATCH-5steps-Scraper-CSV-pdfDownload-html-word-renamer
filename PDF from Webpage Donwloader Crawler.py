import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a', href=True)

    pdf_links = []

    for link in links:
        href = link['href'].lower()
        if href.endswith('.pdf') or 'application/pdf' in link.get('type', ''):
            pdf_links.append(urljoin(url, link['href']))

    return pdf_links, soup

def download_pdf(pdf_url, download_path):
    print(f'urL: {pdf_url}\n')
    filename = os.path.join(download_path, os.path.basename(pdf_url))
    print(f'filename: {filename}')

    with open(filename, 'wb') as pdf_file:
        response = requests.get(pdf_url)
        pdf_file.write(response.content)

def crawl_and_download(url, download_path):
    pdf_links, soup = get_pdf_links(url)
    for pdf_url in pdf_links:
        download_pdf(pdf_url, download_path)

    # Recursively crawl subpages
    subpage_links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True) if not link['href'].startswith('#')]
    for subpage_link in subpage_links:
        crawl_and_download(subpage_link, download_path)

url = "https://www.spireserien.no/"
pdf_folder = "PDFspireserien"

# Create a folder for the PDFs if it doesn't exist
download_path = os.path.join(os.path.expanduser("~"), "Downloads", pdf_folder)
os.makedirs(download_path, exist_ok=True)

crawl_and_download(url, download_path)
