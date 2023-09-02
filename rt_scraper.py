# Import required modules and packages
import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Suppress exceptions in the __del__ method of the undetected Chrome driver
# This is because of a weird error at the end of the script 
# See https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/955
def suppress_exception_in_del(uc):
    old_del = uc.Chrome.__del__

    def new_del(self) -> None:
        try:
            old_del(self)
        except:
            pass
    setattr(uc.Chrome, '__del__', new_del)
suppress_exception_in_del(uc)

# Define a function to switch to a specific review page on Rotten Tomatoes
def switch_review_page(driver: uc.Chrome, page_name: str) -> uc.Chrome:
    page_names = ["All Critics", "Top Critics", "All Audience", "Verified Audience"]
    page_index = page_names.index(page_name) + 1
    # Click on the corresponding review page link using XPath
    driver.find_element(By.XPATH, f"//*[@id=\"reviews\"]/nav/ul/li[{page_index}]/a").click()
    return driver

# Define a function to scrape all critic reviews for a given critic type
def get_all_critics_review(driver: uc.Chrome, critic_type: str) -> pd.DataFrame:
    # Initialize a dictionary to store review data
    reviews = {
        "reviewer":[],
        "tagline":[],
        "text":[],
        "score_all":[]
    }

    # Loop to collect reviews until there are no more pages
    error_flag = 0
    while error_flag==0:
        # Find all review rows on the current page
        review_rows = driver.find_elements(By.CLASS_NAME, "review-row")
        # Iterate through each review row and extract review information
        for item in review_rows:
            review_elements = item.text.split("\n")
            reviews["reviewer"].append(review_elements[0])
            reviews["tagline"].append(review_elements[1])
            reviews["text"].append(review_elements[2])
            reviews["score_all"].append(review_elements[3])

        # Find the "Next" button and attempt to click it
        next_button = driver.find_elements(By.CSS_SELECTOR, "rt-button")[1]
        try:
            next_button.click()
        
        except:
            error_flag = 1

        time.sleep(2)

    # Create a DataFrame from the collected reviews data and add a column for critic type
    df = pd.DataFrame(reviews)
    df["critic_type"] = critic_type

    return df

if __name__=="__main__":
    
    # Initialize ChromeDriverManager to manage ChromeDriver versions
    chrome_manager = ChromeDriverManager()
    version_main = int(chrome_manager.driver.get_browser_version_from_os().split(".")[0])
    driver = uc.Chrome(
        service=Service(ChromeDriverManager().install()),
        version_main=version_main
    )

    dfs = []

    # Open the Rotten Tomatoes page for a specific movie and collect reviews for specified critic types
    driver.get("https://www.rottentomatoes.com/m/oppenheimer_2023/reviews")
    critic_types = ["All Critics", "Top Critics"]
    for critic in critic_types:
        driver = switch_review_page(driver, critic)
        dfs.append(get_all_critics_review(driver, critic))

    # Concatenate the collected DataFrames and save them as a CSV file
    pd.concat(dfs).to_csv("oh_rotten_tomatoes.csv", index=False)
    driver.close()
    driver.quit()