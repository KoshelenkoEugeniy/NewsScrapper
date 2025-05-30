from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def extract_article(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "p"))
            )
        except TimeoutException:
            print("Timeout waiting for page content.")
            driver.quit()
            return None

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        title = soup.find('h1')
        headline = title.get_text(strip=True) if title else 'No headline found'

        paragraphs = soup.find_all("p")
        full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        if not full_text.strip():
            raise ValueError("No article content found.")

        return {
            "headline": headline,
            "content": full_text
        }

    except (WebDriverException, Exception) as e:
        print(f"Error extracting article: {e}")
        return None