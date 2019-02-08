import SMS 
import requests
from bs4 import BeautifulSoup
import re
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# In order to create  the quotes database on Google Spreadsheet, we first
# need to obtain the quotes from a webpage. To do this, we'll use BeautifulSoup
# to scrape the HTML contents of a quotes webpage.

page = requests.get('https://www.inc.com/bill-murphy-jr/here-are-best-inspirational-quotes-for-2018.html')
soup = BeautifulSoup(page.content, 'html.parser')
quotes = soup.find_all(text=re.compile('^[\"]'))

# We need to replace the unicode u'\xa0' with something that can
# be parsed (u' ') or else unicode errors will show up down the line.
for counter, quote in enumerate(quotes):
	quotes[counter] = quote.replace(u'\xa0', u' ')

# Let's set up our credentials and connection to Google Drive & 
# Google Spreadsheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('SpreadsheetExample-0fcdf1e80f81.json', scope)

gc = gspread.authorize(credentials)

# Quote database
quote_db = gc.open('Motivational Quotes Log').worksheet('QuoteDB')

cell_list = quote_db.range('A2:A366')

for counter, cell in enumerate(cell_list):
    cell.value = quotes[counter]

quote_db.update_cells(cell_list)