#!/usr/bin/env python
import sys
from lxml import html
import requests
from datetime import date
from twython import Twython

#***********
#Twitter Authentication from apps.twitter.com
#NOTE: For script to work you'll need to enter in your Twitter Account details below.
apiKey = ''
apiSecret = ''
accessToken = ''
accessTokenSecret = ''
#*********

#Get data from NOAA.gov using lxml
page = requests.get('http://tidesandcurrents.noaa.gov/stationhome.html?id=8534770')
tree = html.fromstring(page.content)
tide_info = tree.xpath('//div[@class="span4 well"]/table[@class="table table-condensed"]/tr/td/text() | //div[@class="span4 well"]/table[@class="table table-condensed"]/tr/td/b/text()')

#Clean up tide_info. NOAA site can place random " ft." strings in list. 
tide_info.remove(" ft.")
tide_info = [item.split(' ft.')[0] for item in tide_info]

#Prepare tweet message
def prepare_twitter_message():
	message_str = "Tide Information for {:%b %d, %Y}: \n".format(date.today())
	while len(tide_info)>0:
		tide_time = tide_info.pop(0)
		tide_type = tide_info.pop(0).title()
		tide_ht = tide_info.pop(0)
		message_str += "{}: {} {} ft\n".format(tide_type, tide_time, tide_ht)
	return message_str

#Configure Tweet and send.
api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)
api.update_status(status=prepare_twitter_message())	
