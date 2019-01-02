import mechanize
import sys
import json
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import selenium.webdriver.support.ui as ui
import time
chrome_options = Options()  
#chrome_options.add_argument("--headless")
br = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'./chromedriver.exe')
br.get('https://www.youtube.com/playlist?list=FLfu72fp0-EvF0_PMq2bLgQA&disable_polymer=1')
wait = ui.WebDriverWait(br,30)
soup = BeautifulSoup(br.page_source, "html.parser")

count = 0
video_list = []

for tr in soup.findAll('tr'):
	
	if tr.has_attr('data-video-id'):

		title = tr['data-title']

		# Add removed videos to list
		if 'Private' in title or 'Deleted' in title:
			print tr['data-title'] + ' - ' + tr['data-video-id']
			video_list.append(tr['data-video-id'])
	count = count + 1


	# Load next batch of videos
	#video = br.find_element_by_xpath('//*[@id="pl-load-more-destination"]/tr['+str(count)+']')
	#button = wait.until(lambda br: br.find_element_by_xpath('//*[@id="pl-video-list"]/button'))

	#if video:

	#	button.click()
	#	count = 0



snapshots = []
remaining = []

# Check if Wayback Machine has video title saved
for video in video_list:
	url = 'http://archive.org/wayback/available?url=https://www.youtube.com/watch?v=' + video
	br.get(url)
	json_data = json.loads(br.find_element_by_tag_name('pre').text)

	# Has snapshot; add to list
	if json_data["archived_snapshots"]:
		snapshots.append(json_data["archived_snapshots"]['closest']['url'])
	# Save ID for later google scraping
	else:
		remaining.append(video)

print('\n'.join(snapshots))
	
for video in snapshots:
	br.get(video)
	snap = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')
	
	# Go to earliest screenshot instead
	while snap == "":
		br.find_element_by_xpath('//*[@id="wm-ipp-inside"]/div[1]/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[1]').click()
		snap = br.find_element_by_xpath("//meta[@name='title']").get_attribute('content')

	print snap



br.quit()