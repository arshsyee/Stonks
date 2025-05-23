# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_trades_for(ticker, headless=True, timeout=10):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get("https://www.capitoltrades.com/trades")
        search_sel = "input[placeholder='Search']"  # adjust if needed
        search_input = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, search_sel))
        )
        search_input.clear()
        search_input.send_keys(ticker)
        search_input.send_keys(Keys.ENTER)

        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        soup  = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.select_one("table")

        headers = [th.get_text(strip=True) for th in table.select("thead th")]
        rows    = []
        for tr in table.select("tbody tr"):
            cols = [td.get_text(strip=True) for td in tr.find_all("td")]
            rows.append(dict(zip(headers, cols)))

        return rows

    finally:
        driver.quit()