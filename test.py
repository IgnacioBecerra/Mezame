from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import selenium.webdriver.support.ui as ui
import time
import re
chrome_options = Options()  
#chrome_options.add_argument("--headless")

start_time = time.time()
br = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'./chromedriver.exe')
wait = ui.WebDriverWait(br,3)

def chunkErrorCheck():

	while True:
		try:
			text = br.find_element_by_xpath('//*[@id="main-message"]/h1/span')

			if text:
				br.find_element_by_xpath('//*[@id="reload-button"]').click()
		except:
			break

unarchived = []
with open('./notFound.txt') as f:
    unarchived = [tuple(map(str, i.split(' '))) for i in f]


for i in unarchived:
	print i[0], i[1]


for index, video in unarchived:
	url = video
	br.get(url)
	chunkErrorCheck()

	# Get remains of title
	title = br.find_element_by_xpath('//*[@id="unavailable-message"]').text
	title = re.search('"(.*)..."', title).group(1)

	# Search for mirror video with ID
	title = title + " " + video
	print title

elapsed_time = time.time() - start_time
br.quit()