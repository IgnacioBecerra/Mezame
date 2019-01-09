from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import selenium.webdriver.support.ui as ui
import time
import re
chrome_options = Options()  
#chrome_options.add_argument("--headless")
br = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'./chromedriver.exe')

with open('./links') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
snapshots = [x.strip('\n') for x in content] 

# Scrape Wayback Machine for video titles using found video IDs
for video in snapshots:
	br.get(video)
	title = ''
	
	try:
		title = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')
		print title
		continue
	except:
		pass
	
	# Setting maximum tries if Wayback loops back (it's a glitchy website)
	x = br.find_element_by_xpath('//*[@id="wm-nav-captures"]/a').get_attribute('text')
	totalSnaps = re.findall('\d+', x[0])
	totalSnaps = int(totalSnaps[0])
	tries = 0

	# Go to earliest snapshot instead if most recent is unavailable
	while title == "" and tries < totalSnaps:

		# Get title 
		try:
			title = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')
			print title + " YUP"
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


for video in remaining:
	url = 'https://www.youtube.com/watch?v=' + video + '&disable_polymer=1'
	br.get(url)

	# Get remains of title
	title = br.find_element_by_xpath('//*[@id="unavailable-message"]').text
	title = re.search('"(.*)..."', title).group(1)

	# Search for mirror video with ID
	title = title + " " + video
	print title


br.quit()