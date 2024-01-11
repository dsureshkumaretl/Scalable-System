# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 22:43:10 2023

@author: Siureshkumar Durairaj
"""

import requests
from bs4 import BeautifulSoup
import re
import os

# Define the working directory for saving the books
working_dir = './books'
books_urls = {
'Just_So_Stories': 'https://www.gutenberg.org/cache/epub/32488/pg32488.txt',
'The_Jungle_Book': 'https://www.gutenberg.org/cache/epub/236/pg236.txt',
'With_The_Night_Mail': 'https://www.gutenberg.org/cache/epub/29135/pg29135.txt',
'The_Man_Who_Would_Be_King': 'https://www.gutenberg.org/files/8147/8147-0.txt',
'Captains_Courageous': 'https://www.gutenberg.org/cache/epub/2186/pg2186.txt',
'Kipling_Stories_and_Poems_Every_Child_Should_Know_Book2':'https://www.gutenberg.org/cache/epub/30568/pg30568.txt',
'The_Light_that_Failed':'https://www.gutenberg.org/files/2876/2876-0.txt',
'The_Phantom_Rickshaw_and_Other_Ghost':'https://www.gutenberg.org/files/2806/2806-0.txt',
'The_Second_Jungle_Book':'https://www.gutenberg.org/files/1937/1937-0.txt',
'Plain_Tales_from_the_Hills':'https://www.gutenberg.org/files/1858/1858-0.txt',
'A_Diversity_of_Creatures':'https://www.gutenberg.org/cache/epub/13085/pg13085.txt',
'Barrack_Room_Ballads':'https://www.gutenberg.org/files/2819/2819-0.txt',
'Rewards_and_Fairies':'https://www.gutenberg.org/files/556/556-0.txt',
'Puck_of_Pooks_Hill':'https://www.gutenberg.org/cache/epub/557/pg557.txt',
'Kim':'https://www.gutenberg.org/cache/epub/2226/pg2226.txt'
}

# Define a function to download a book from its URL and save it to the working directory
def download_book(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Download the books to the working directory
os.makedirs(working_dir, exist_ok=True)
for book, url in books_urls.items():
    filename = os.path.join(working_dir, book + '.txt')
    download_book(url, filename)

# Preprocess the books
books = {}
for book in os.listdir(working_dir):
    filename = os.path.join(working_dir, book)
    with open(filename, 'r', encoding='utf-8') as f:
        book_text = f.read()
    # Remove header and footer text
    book_text = re.sub(r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK.*\*\*\*\n?", "", book_text)
    book_text = re.sub(r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK.*\*\*\*\n?", "", book_text)
    # Remove chapter headings and numbers
    book_text = re.sub(r"\n\d+\n", "\n", book_text)
    book_text = re.sub(r"\nCHAPTER \w+\n", "\n", book_text)
    book_text = re.sub(r"\nCHAPTER \d+\n", "\n", book_text)
    book_text = re.sub(r"\nVOLUME \d+\n", "\n", book_text)
    # Remove extra newlines
    book_text = re.sub(r"\n+", "\n", book_text)
    book_text = book_text.strip()
    books[book[:-4]] = book_text
    

#Testing the Extraction Reading one Book
#print('The File The Jungle Book is read properly as shown below \n')
#print(books['The_Jungle_Book'])
folder_path = '/home/hduser/sspca/books'
target_string1 = '*** START OF THIS PROJECT '
target_string2= '*** START OF THE PROJECT '
target_string3= '***START OF THE PROJECT ' 
def remove_lines_before_string(file_path, string):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if string in line:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines[i:])
            break

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path) and file_name.endswith('.txt'):
        remove_lines_before_string(file_path, target_string1)
        remove_lines_before_string(file_path, target_string2)
        remove_lines_before_string(file_path, target_string3)