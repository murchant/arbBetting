from lxml import html
from lxml import etree
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
page = requests.get('https://www.oddschecker.com/football/english/premier-league/leicester-v-tottenham/winner', verify=False)
tree = html.fromstring(page.content)

homeTeamName = tree.xpath('//*[@id="t1"]/tr[1]/td[1]/span[1]/@data-name')
awayName = tree.xpath('//*[@id="t1"]/tr[3]/td[1]/span[1]/@data-name')
homeOdd = {}						#dictionary containing all home odds + bookie
drawOdd = {}						#dictionary containing all draw odds + bookie
awayOdd = {}						#dictionary containing all away odds + bookie

#Changes string representation of odds into decimal odds
def sFracToFloat(fracStr):
	if '/' in fracStr:
		numbers = fracStr.split("/")
		decimal= (float(numbers[0])/float(numbers[1])) + 1
		return decimal
	else:
		dec = float(fracStr) + 1
		return dec

#Odd as percentage
def percentage(oddFloat):
	return 100/oddFloat

# Calcualte whether the created market is over/under arb, and if so....
# ... return percentage
def total(h, d, a):
	return h+d+a

#runs through all combinations of home, draw, away, and extracts all....
#... combinations which are arbs, puts them in dict and returns dict.
def extractArbs(homes, draws, aways):
	arb = {}
	arbs = {}
	count=0
	for x in homes:
		for y in draws:
			for z in aways:
				h=percentage(sFracToFloat(homes[x]))
				d=percentage(sFracToFloat(draws[y]))
				a=percentage(sFracToFloat(aways[z]))
				#print total(h,d,a)
				if total(h,d,a)<100:
					arb[x]=h
					arb[y]=d
					arb[z]=a
					arbs[count] = arb
					count+=1


for i in range(2, 10):
	home = '//*[@id="t1"]/tr[1]/td[' + str(i) +']/text()'
	draw = '//*[@id="t1"]/tr[2]/td['+ str(i) +']/text()'
	away = '//*[@id="t1"]/tr[3]/td['+ str(i) +']/text()'
	bookie = '//*[@id="oddsTableContainer"]/table/thead/tr[4]/td['+str(i)+']/aside/a/@title'
	homeTeam = tree.xpath(home)
	drawTeam = tree.xpath(draw)
	awayTeam = tree.xpath(away)
	bookieName = tree.xpath(bookie)
	homeOdd[bookieName[0]]=homeTeam[0]								
	drawOdd[bookieName[0]]=drawTeam[0]								
	awayOdd[bookieName[0]]=awayTeam[0]

for x in homeOdd:
	# 	testList = percentage(sFracToFloat(homeOdd[x]))
	# 	print x, homeOdd[x], drawOdd[x], awayOdd[x] 
	# 	print x, 'H:', homeOdd[x], 'D:', drawOdd[x], 'A:', awayOdd[x], percentage(sFracToFloat(homeOdd[x])), percentage(sFracToFloat(drawOdd[x])), percentage(sFracToFloat(awayOdd[x]))
	myArbDictionary = extractArbs(homeOdd, drawOdd, awayOdd)




#def calculateArb(homeOdd, drawOdd,awayOdd):
#	for i in homeOdd:
#		homePer = sFracToInt(homeOdd[i])




#bookie 
#//*[@id="oddsTableContainer"]/table/thead/tr[4]/td[2]/aside/a/title
# #win 
# //*[@id="t1"]/tr[1]/td[2]

# #draw
# //*[@id="t1"]/tr[2]/td[2]

# #lose 
# //*[@id="t1"]/tr[3]/td[2]
