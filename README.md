# Rotten Tomatoes Review Scraper

This Python script uses Selenium and undetected_chromedriver to scrape critic reviews from Rotten Tomatoes for a specific movie and save the data to a CSV file. The script is designed to handle exceptions and includes a workaround for a known issue with undetected_chromedriver.

## Prerequisites

Before running the script, make sure you have the following Python packages installed:

- pandas
- selenium
- webdriver_manager
- undetected_chromedriver

You can install these packages using pip:
`pip install time pandas undetected_chromedriver selenium webdriver_manager`

## Usage

1. Clone this repository or download the script (`rotten_tomatoes_scraper.py`) to your local machine.
2. Open the script in a text editor and make any necessary adjustments, such as specifying the movie URL and desired critic types.
3. Run the script using Python:
`python rotten_tomatoes_scraper.py`

The script will open a headless Chrome browser, navigate to the specified movie's Rotten Tomatoes page, collect reviews for the specified critic types, and save the data to a CSV file named `oh_rotten_tomatoes.csv`.

## Suppressing Exceptions

The script includes a workaround for a known issue with undetected_chromedriver that causes exceptions in the `__del__` method. These exceptions are suppressed to prevent script failure.

## Acknowledgments

- [undetected_chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver): A ChromeDriver manager that helps bypass bot detection mechanisms.


