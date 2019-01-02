from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import selenium.webdriver.support.ui as ui
import time
import re
chrome_options = Options()  
#chrome_options.add_argument("--headless")
br = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'./chromedriver.exe')


br.get('https://www.youtube.com/watch?v=cXTmYe6UxZM&disable_polymer=1')

t = br.find_element_by_xpath('//*[@id="unavailable-message"]').text
x = re.search('"(.*)..."', t).group(1)
print x
br.quit()