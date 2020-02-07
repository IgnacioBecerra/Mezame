import time
from selenium import webdriver

driver = webdriver.Chrome('./chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://web.archive.org/web/*/youtube.com/watch?v=GPo4LTuQ71M');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()