from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import selenium.webdriver.support.ui as ui
import time
chrome_options = Options()  
#chrome_options.add_argument("--headless")
br = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'./chromedriver.exe')


br.get('http://web.archive.org/web/20110806081708/http://www.youtube.com/watch?v=gtm8PDOT5f4&gl=US&hl=en&amp;has_verified=1')
snap = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')

# Go to earliest screenshot instead
while snap == "":
	br.find_element_by_xpath('//*[@id="wm-ipp-inside"]/div[1]/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[1]').click()
	snap = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')

print snap


br.quit()