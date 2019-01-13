# Motivational Quotes Texter
#### A simple program that texts you a motivational quote every day.

This application utilizes the Google Spreadsheet API (gspread) as a mini-database in order to store the quotes needed for the application function, which is sending SMS to a specified phone number. I used the BeautifulSoup library in order to scrape and parse the [Motivational Quotes Web Page](https://www.inc.com/bill-murphy-jr/here-are-best-inspirational-quotes-for-2018.html) for our quotes. These quotes are then stored on the [Motivational Quotes Spreadsheet](https://docs.google.com/spreadsheets/d/1kAapNKCMRk3ARRqGi4Zx2IpGlHL16VQuyb4a08xxVIY/edit?usp=sharing). The first sheet contains all the quotes in the database, and the second sheet contains the date each quote corresponds to.
