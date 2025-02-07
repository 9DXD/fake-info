import requests
from bs4 import BeautifulSoup
import random
import re
import tkinter as tk
from tkinter import scrolledtext

def scrape_fake_identity():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get('https://www.fakenamegenerator.com', headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}

    # Extract name and address
    address_div = soup.find('div', class_='address')
    if address_div:
        data['Name'] = address_div.find('h3').get_text(strip=True)
        data['Address'] = ' '.join(address_div.find('div', class_='adr').stripped_strings)

    # Process all dl-horizontal elements
    for dl in soup.find_all('dl', class_='dl-horizontal'):
        dt = dl.find('dt')
        dd = dl.find('dd')
        if dt and dd:
            key = dt.get_text(strip=True).rstrip(':')
            value = dd.get_text(strip=True)
            
            # Special handling for SSN
            if key == 'SSN':
                ssn_match = re.match(r'^(\d{3}-\d{2}-)(\d{4}|X{4})', value)
                if ssn_match:
                    prefix = ssn_match.group(1)
                    suffix = ssn_match.group(2)
                    if 'X' in suffix:
                        suffix = ''.join(random.choices('0123456789', k=4))
                    value = f"{prefix}{suffix}"
            
            data[key] = value

    return data

def show_info_popup(data):
    root = tk.Tk()
    root.title("Generated Fake Information")
    
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
    text_area.pack(padx=10, pady=10)
    
    # Display basic info
    text_area.insert(tk.INSERT, f"NAME: {data.get('Name', 'N/A')}\n")
    text_area.insert(tk.INSERT, f"ADDRESS: {data.get('Address', 'N/A')}\n\n")
    
    # Display other details
    sections = {
        'Personal': ['SSN', 'Birthday', 'Age', 'Tropical zodiac', 'Mother\'s maiden name'],
        'Contact': ['Phone', 'Country code', 'Geo coordinates'],
        'Online': ['Username', 'Password', 'Website', 'Browser user agent'],
        'Financial': ['Visa', 'Expires', 'CVV2'],
        'Employment': ['Company', 'Occupation'],
        'Physical': ['Height', 'Weight', 'Blood type'],
        'Tracking': ['UPS tracking number', 'Western Union MTCN', 'MoneyGram MTCN'],
        'Other': ['Favorite color', 'Vehicle']
    }

    for section, fields in sections.items():
        text_area.insert(tk.INSERT, f"=== {section} ===\n")
        for field in fields:
            value = data.get(field, 'N/A')
            text_area.insert(tk.INSERT, f"{field}: {value}\n")
        text_area.insert(tk.INSERT, "\n")

    text_area.configure(state='disabled')
    root.mainloop()

if __name__ == "__main__":
    fake_data = scrape_fake_identity()
    if fake_data:
        show_info_popup(fake_data)
    else:
        print("Failed to retrieve data")
