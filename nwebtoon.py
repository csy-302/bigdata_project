from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# Optional: for waiting
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time # For simple waits if needed

# 1. WebDriver Setup
# Download ChromeDriver executable and specify its path, or use Service
# For modern Selenium (4+), Service is preferred. Ensure chromedriver is in your PATH or specify service.
# service = Service('/path/to/chromedriver') # Uncomment and modify if chromedriver is not in PATH
# driver = webdriver.Chrome(service=service)
# Simpler if chromedriver is in PATH:
driver = webdriver.Chrome() # Assuming chromedriver is in PATH

# 2. Navigate
url = 'https://comic.naver.com/webtoon?tab=mon'
driver.get(url)

# 3. Wait (Optional but Recommended)
# Wait for the main list container to be present
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.list_toon'))
    )
    # Small additional sleep might help for images to load, though not strictly necessary for text/attributes
    time.sleep(2)
except Exception as e:
    print(f"Error waiting for page to load: {e}")
    driver.quit()
    exit()


# 4. Find all webtoon items
webtoon_items = driver.find_elements(By.CSS_SELECTOR, 'ul.list_toon li')

# 5. Extract data
webtoon_data = []
print(f"Found {len(webtoon_items)} webtoons.") # Debugging print

for item in webtoon_items:
    try:
        # Selectors based on inspection
        thumbnail_img = item.find_element(By.CSS_SELECTOR, 'div.const_area a.img img')
        thumbnail_url = thumbnail_img.get_attribute('src') if thumbnail_img else 'N/A'

        title_elem = item.find_element(By.CSS_SELECTOR, 'div.info a.title')
        title = title_elem.text if title_elem else 'N/A'

        author_elem = item.find_element(By.CSS_SELECTOR, 'div.info span.author')
        author = author_elem.text if author_elem else 'N/A'

        rating_elem = item.find_element(By.CSS_SELECTOR, 'div.info span.score')
        rating = rating_elem.text if rating_elem else 'N/A'

        webtoon_data.append({
            'thumbnail_url': thumbnail_url,
            'title': title,
            'author': author,
            'rating': rating
        })
    except Exception as e:
        # Print error for specific item to help debugging
        print(f"Error processing an item: {e}")
        # You might want to skip this item or log it differently
        continue # Skip to the next item if one fails


# 6. Close browser
driver.quit()

# 7. Print or process data
# print(webtoon_data) # Print the whole list (can be long)

# Print nicely
print("\n--- 네이버 월요웹툰 데이터 ---")
for data in webtoon_data:
    print(f"타이틀: {data['title']}")
    print(f"작가명: {data['author']}")
    print(f"평점: {data['rating']}")
    print(f"썸네일 주소: {data['thumbnail_url']}")
    print("-" * 20)

print("데이터 수집 완료.")