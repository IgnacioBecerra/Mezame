import mechanize
import sys
import json
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import selenium.webdriver.support.ui as ui
import time
chrome_options = Options()
#chrome_options.add_argument("--headless")


start_time = time.time()
br = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'./chromedriver.exe')
br.get('https://www.youtube.com/playlist?list=FLfu72fp0-EvF0_PMq2bLgQA&disable_polymer=1')
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



count = 1
video_list = []
video_titles = []

# Click next button to load more videos
for i in range(1, 5):
	time.sleep(1)
	button = wait.until(lambda br: br.find_element_by_xpath('//*[@id="pl-video-list"]/button')).click()
	
# Go through each video title, and collect the ID's of removed videos
soup = BeautifulSoup(br.page_source, "html.parser")
for tr in soup.findAll('tr'):
	
	if tr.has_attr('data-video-id'):

		title = tr['data-title']

		# Add removed videos to list
		if 'Private' in title or 'Deleted' in title:
			print str(count) + " " + tr['data-title'] + ' - ' + tr['data-video-id']
			video_list.append((count, tr['data-video-id']))
	count = count + 1

snapshots = []
unarchived = []

# Check if Wayback Machine has video title saved
for index, video in video_list:
	url = 'http://archive.org/wayback/available?url=https://www.youtube.com/watch?v=' + video
	br.get(url)
	json_data = json.loads(br.find_element_by_tag_name('pre').text)

	# Has snapshot; add most recent to list
	if json_data["archived_snapshots"]:
		snapshots.append((index, json_data["archived_snapshots"]['closest']['url']))
	
	# Save ID for later google scraping
	else:
		print "No wayback " + str(index) + " " + video
		unarchived.append((index, video))


for i in snapshots:
	print i[0], i[1]

# Scrape Wayback Machine for video titles using found video IDs
for index, video in snapshots:
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
	while True:
		try:
			x = wait.until(lambda br: br.find_element_by_xpath('//*[@id="wm-nav-captures"]/a').get_attribute('text'))
			break
		except:
			br.refresh()
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
				print str(index) + " " + title
				video_titles.append((index, title))
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
		print "appending..." + str(index) + " " + video
		unarchived.append((index,video))

elapsed_time = time.time() - start_time
print elapsed_time

for i in unarchived:
	print i[0], i[1]

br.quit()

for index, video in unarchived:

	# Access Wayback
	if "youtube" in video:
		url = re.search('?v=(.*)', video).group(1)
		url = 'http://web.archive.org/web/*/https://www.youtube.com/watch?v=' + url
		br.get(url)
		title = ''
		wait.until(lambda br: br.find_element_by_xpath('//*[@id="wbMetaCaptureDates"]/span/a[1]')).click()

		# Get title 
		try:
			title = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')

			if title != '':
				print str(index) + " " + title
		except:
			pass



	
	
	else:
		br.get('youtube.com/watch?v=' + video)
		
		# Get remains of title
		title = br.find_element_by_xpath('//*[@id="unavailable-message"]').text
		title = re.search('"(.*)..."', title).group(1)


		# Search for mirror video with ID
		title = title + " " + video
		print title

	'''
		Scenarios:

		No wayback
		>Go to youtube page
		>Get title
		>search ID + title
		>else ID

		
		Wayback
		>Go to earliest
		>Check for title
		>If no title, search ID only
		>else search ID + title
	'''

	chunkErrorCheck()

	

elapsed_time = time.time() - start_time
br.quit()