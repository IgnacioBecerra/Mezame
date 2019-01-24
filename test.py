from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import selenium.webdriver.support.ui as ui
import time
import re
chrome_options = Options()  
#chrome_options.add_argument("--headless")
start_time = time.time()
br = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'./chromedriver.exe')

def chunkErrorCheck():

	while True:
		try:
			text = br.find_element_by_xpath('//*[@id="main-message"]/h1/span')

			if text:
				br.find_element_by_xpath('//*[@id="reload-button"]').click()
		except:
			break

remaining = []
with open('./links') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
snapshots = [x.strip('\n') for x in content] 

# Scrape Wayback Machine for video titles using found video IDs
for video in snapshots:
	br.get(video)
	chunkErrorCheck()
	title = ''
	
	try:
		title = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')
		
		# Go to next video if title is found
		if title != "":
			print title
			continue
	except:
		pass
	
	# Setting maximum tries if Wayback loops back (it's a glitchy website)
	x = br.find_element_by_xpath('//*[@id="wm-nav-captures"]/a').get_attribute('text')
	totalSnaps = re.findall('\d+', x)
	totalSnaps = int(totalSnaps[0])
	tries = 0

	# Go to earliest snapshot instead if most recent is unavailable
	while title == "" and tries < totalSnaps:
		chunkErrorCheck()

		# Get title 
		try:
			title = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')

			if title != "":
				print title
				continue
		except:
			pass
		
		# check if there are more snapshots if current title is null
		try:
			br.find_element_by_xpath('//*[@id="wm-ipp-inside"]/div[1]/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[1]').click()
		except:
			break

		tries = tries + 1

	# Print current title for confirmation
	if title == "":
		print "appending..."
		remaining.append(video)

elapsed_time = time.time() - start_time
print elapsed_time

for video in remaining:
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
print elapsed_time
br.quit()
