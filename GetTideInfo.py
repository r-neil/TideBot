from lxml import html
import requests
from datetime import date

page = requests.get('http://tidesandcurrents.noaa.gov/stationhome.html?id=8534770')
tree = html.fromstring(page.content)

tides = tree.xpath('//div[@class="span4 well"]/table[@class="table table-condensed"]/tr/td/text()')
high_tide = tree.xpath('//div[@class="span4 well"]/table[@class="table table-condensed"]/tr/td/b/text()')

def prepare_twitter_message():
	today_str = "Tide Information for {:%b %d, %Y}: \n".format(date.today())
	low_tide_am = "Low: {} - {}\n".format(tides[0], tides[2])
	high_tide_am = "High: {} - {}\n".format(tides[3], tides[5])
	low_tide_pm = "Low: {} - {}\n".format(tides[6], tides[8])
	high_tide_pm = "High: {} - {} ft.".format(high_tide[0], high_tide[2])
	print(today_str + low_tide_am + high_tide_am + low_tide_pm + high_tide_pm)

prepare_twitter_message()
