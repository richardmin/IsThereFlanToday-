'''
Author: Richard Min (richardmin97@gmail.com)
Uses httplib2 and BeautifulSoup to prase the riot skins sales webpage, reading what it has already found from a text file and comparing that
to what is new on the page, printing that out and updating the text file
This code is licensed under MIT creative license.
'''

#!/usr/bin/env python
import httplib2
from BeautifulSoup import BeautifulSoup

class PageNotFound(RuntimeError): pass


class FlanScraper(object):
	def __init__(self, url="http://menu.ha.ucla.edu/foodpro/", timeout=15):
		self.url, self.timeout = url, int(timeout)

	def fetch_sales(self):
		http = httplib2.Http(timeout=self.timeout)
		headers, content = http.request(self.url)

		if not headers.get('status') == '200':
			raise PageNotFound("Could not fetch page from '%s'. Got %s." % (self.url, headers['status']))

		return content

	def parse_sales(self, content):
		soup = BeautifulSoup(content)
		# print soup
		raw = soup.findAll("a" , { "class" : "menuloclink" })
		for line in raw:
			print line
			if len(line.contents[0]) < 15:
				continue
			if not line.contents[0] == "FEAST at Rieber":
				continue
			processed.append(str(line['href']))
		return 
		# return processed

	def get_sales(self):
		content = self.fetch_sales()
		return self.parse_sales(content)

	def newSales(self):
		releases = self.get_sales()
		
		text_file = open('theresflantoday.txt', 'r')
		rawlines = text_file.readlines()
		lines = []
		for rawline in rawlines:
			lines.append(rawline[:-1])
		diff = []
		for release in releases:
			if not release in lines:
				diff.append(release)
			
		return diff
		
	def fetch_salepage(self, url):
		http = httplib2.Http(timeout=self.timeout)
		headers, content = http.request('http://menu.ha.ucla.edu/foodpro/'+url)

		if not headers.get('status') == '200':
			raise PageNotFound("Could not fetch page from '%s'. Got %s." % ('http://menu.ha.ucla.edu/foodpro/'+url, headers['status']))

		return content
		
	def parse_salepage(self, content):
		soup = BeautifulSoup(content)
		print "parse_salepage called"
#		rawprices = soup.findAll("strike")
		raw = soup.findAll("li", { "class" : "level2"})

		for line in raw:
			if len(line['title']) < 12:
				continue
			if not line['title'][:12] == "FEAST at Rieber":
				print "there is flan today"
				return "there is flan today"
		return processed
		print "there is no flan today"
		return "there is no flan today"
		
	def get_salepage(self, url):
		content = self.fetch_salepage(url)
		return self.parse_salepage(content)
		
	def processSales(self): 
		urls = self.newSales()
		prepend = ''
		
		for url in urls:
			print self.get_salepage(url)
			prepend = prepend + '\n'
		with file('theresflantoday.txt', 'w') as modified: modified.write(prepend)

			
if __name__ == '__main__':
	scraper = FlanScraper()
	# releases = scraper.get_sales()
	scraper.processSales()