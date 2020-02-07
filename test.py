from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import selenium.webdriver.support.ui as ui
import time
import re
chrome_options = Options()  
#chrome_options.add_argument("--headless")
start_time = time.time()
br = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'./chromedriver.exe')
wait = ui.WebDriverWait(br,100)

def chunkErrorCheck():

	while True:
		try:
			text = br.find_element_by_xpath('//*[@id="main-message"]/h1/span')

			if text:
				br.find_element_by_xpath('//*[@id="reload-button"]').click()
		except:
			pass

		try:
			text = br.find_element_by_xpath('/html/head/title').get_attribute('innerhtml')

			if '502' in text:
				br.refresh()
		except:
			break

search_list = []
unarchived = []
with open('./notFound.txt') as f:
    unarchived = [tuple(map(str, i.replace('\n','').split(' '))) for i in f]

for i in unarchived:
	print(i[0], i[1])


for index, videoID in unarchived:

	title = ''

	# Access Wayback
	if "youtube" in videoID:
		url = videoID.partition("?v=")[2]
		url = 'http://web.archive.org/web/*/https://www.youtube.com/watch?v=' + url
		br.get(url)
		title = ''
		br.implicitly_wait(10)

		while True:
			print("looping")
			
			try:
				br.find_element_by_xpath('//*[@id="react-wayback-search"]/div[2]/span/a[1]').click()
			except:
				pass
				
			try:
				br.find_element_by_xpath('//*[@id="react-wayback-search"]/div[2]/a').click()
			except:
				break

		print("Before chunk")
		#chunkErrorCheck()
		print("After chunk")

		br.implicitly_wait(10)

		# Get title 
		try:
			print("first try")
			title = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')

			if title != '':
				print(str(index) + " " + title)

			print('second')
			title = br.find_element_by_xpath('//*[@id="unavailable-message"]').text
			# ^ http://web.archive.org/web/20140803133656/https://www.youtube.com/watch?v=AfOML-DgMvA
			print(str(index) + " " + title)
			
		except:


			print("HERE")
			title = br.find_elements_by_xpath("/html/head/title")[0].text

			if title != '':
				print(str(index) + " " + title)


	else:
		br.get('https://www.youtube.com/watch?v=' + videoID + '&disable_polymer=1')
		
		try:
			# Get remains of title
			title = br.find_element_by_xpath('//*[@id="unavailable-message"]').text
			title = re.search('"(.*)..."', title).group(1)

			# Search for mirror videoID with ID
			print(title + " " + videoID)
		
		except:
			# No videoID title available, search
			print(videoID)

	search_list.append((index, title, videoID))

for i in search_list:
	print(i[0], i[1], i[2])

br.quit()
