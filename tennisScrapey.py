from lxml import html
from lxml import etree
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

page2 = page = requests.get('https://www.oddschecker.com/tennis', verify=False)
tree2 = html.fromstring(page2.content)

homeOdd = {}						#dictionary containing all home odds + bookie
drawOdd = {}						#dictionary containing all draw odds + bookie
awayOdd = {}						#dictionary containing all away odds + bookie
bookieParam = {}

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
def extractArbs(homes, draws, aways, treeT, fixture):
	
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
					#print total(h,d,a)
					arb = [fixture[0]+' vs '+fixture[1] + ' | '+x+': '  + homes[x],  y+': ' + draws[y], z+': '+aways[z]]
					# arb[0]=homes[x]
					# arb[1]=draws[y]
					# arb[2]=aways[z]
					arbs[count] = arb
					#print arbs[count]
					count+=1
	return arbs

myArbDictionary = {}
for i in range(3, 10):
	linkName = '//*[@id="fixtures"]/div/table/tbody/tr['+str(i)+']/td[5]/a/@href'
	link = tree2.xpath(linkName)
	#print link

	if len(link)>0:
		page = requests.get('https://www.oddschecker.com'+link[0], verify=False)
		treeT = html.fromstring(page.content)
		homeTeamName = treeT.xpath('//*[@id="t1"]/tr[1]/td[1]/span[1]/@data-name')
		awayName = treeT.xpath('//*[@id="t1"]/tr[3]/td[1]/span[1]/@data-name')
		fixture = homeTeamName+awayName
		#print homeTeamName, 'vs', awayName
#for loop to check each odds for a given match with different bookmakers
	for i in range(2, 10):
		home = '//*[@id="t1"]/tr[1]/td[' + str(i) +']/text()'
		draw = '//*[@id="t1"]/tr[2]/td['+ str(i) +']/text()'
		away = '//*[@id="t1"]/tr[3]/td['+ str(i) +']/text()'
		bookie = '//*[@id="oddsTableContainer"]/table/thead/tr[4]/td['+str(i)+']/aside/a/@title'
		homeTeam = treeT.xpath(home)
		drawTeam = treeT.xpath(draw)
		awayTeam = treeT.xpath(away)
		bookieName = treeT.xpath(bookie)
		if len(homeTeam)>0:
			homeOdd[bookieName[0]]=homeTeam[0]
		if len(drawTeam)>0:	
			drawOdd[bookieName[0]]=drawTeam[0]
		if len(awayTeam)>0:								
			awayOdd[bookieName[0]]=awayTeam[0]

		for x in homeOdd:
			# 	testList = percentage(sFracToFloat(homeOdd[x]))
			# 	print x, homeOdd[x], drawOdd[x], awayOdd[x] 
			# 	print x, 'H:', homeOdd[x], 'D:', drawOdd[x], 'A:', awayOdd[x], percentage(sFracToFloat(homeOdd[x])), percentage(sFracToFloat(drawOdd[x])), percentage(sFracToFloat(awayOdd[x]))
			myArbDictionary = extractArbs(homeOdd, drawOdd, awayOdd, treeT,fixture)

		# Printing of the arb dwictionary, may be wrong as you wrote it wwithout internet or testing!!!!!!!!!!!!!!!
		for y in myArbDictionary:
			print y, myArbDictionary[y]
			print '    '





#bookie 
#//*[@id="oddsTableContainer"]/table/thead/tr[4]/td[2]/aside/a/title
# #win 
# //*[@id="t1"]/tr[1]/td[2]

# #draw
# //*[@id="t1"]/tr[2]/td[2]

# #lose 
# //*[@id="t1"]/tr[3]/td[2]
