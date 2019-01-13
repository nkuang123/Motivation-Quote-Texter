import SMS 
import random
import gspread
import schedule
import time
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Let's set up our credentials and connection to Google Drive & 
# Google Spreadsheet

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('SpreadsheetExample-0fcdf1e80f81.json', scope)

gc = gspread.authorize(credentials)

# For now, we're going to mash everything together into one function. 
# send_quote() will pull the quote of the day from the 'QuoteDB' sheet,
# write to the 'QuoteLog' sheet, and then fire the quote of the day to 
# the phone number through SMS.
def send_quote():
	# Now, we'll initialize the specific worksheet we want to work with;
	# in our case, this will be the quotes log. In this log, all the quotes
	# will be in column 1 of the 'QuoteDB' subsheet. 
	# NOTE: Google Spreadsheets are indexed starting at 1, and 
	# in Cartesian coordinate form e.g. for B1 -> (1, 2)

	# Quote database
	quote_db = gc.open('2019QuotesLog').worksheet('QuoteDB')

	# Quote log that we will write to with data/time and quote information
	quote_db_log = gc.open('2019QuotesLog').worksheet('QuoteLog')

	# Some constants
	quote_col = 1
	db_size = len(quote_db.col_values(quote_col))

	# db_size + 1 due to 1-indexing, and + 1 again since we start at 
	# index 2
	row_index = 1 + random.randrange(db_size)

	quote_of_the_day = quote_db.cell(row_index, quote_col).value

	# WRITING TO THE QUOTE LOG
	# This is simple. We already have the quote of the day in 
	# quote_of_the_day. Now all we need to do is write that
	# information, along with the datetime onto the next successive 
	# row in QuoteLog.
	# Format: DATETIME QUOTE
	date_string = date_string_today()
	quote_db_log.append_row([date_string, quote_of_the_day])

	# Now that we've appended that information to the quote log, 
	# we can delete that quote row from the database

	quote_db.delete_row(row_index)

	# Debugging 
	print(quote_of_the_day)
	print("Row Index: " + str(row_index))

	# Finally, to send the quote to the phone number in SMS
	# SMS.send(quote_of_the_day)

# date_string_today() returns the current date and time in a 
# string format, e.g. Jan 1, 2019 (12:49:03 PM)
def date_string_today():
	today = datetime.now()
	return today.strftime("%b %d, %Y (%I:%M:%S %p)")

# In order to have the script send messages at specified times, we 
# will use the schedule library.
schedule.every(5).seconds.do(send_quote)

while True:
	# gc.login() will refresh the access token for the Google Spreadsheet API,
	# else we'll receive error 401 (token expired)
	gc.login()
	schedule.run_pending()
	time.sleep(10)


