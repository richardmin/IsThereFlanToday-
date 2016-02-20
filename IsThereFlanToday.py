'''
Author: Richard Min (richardmin97@gmail.com)
Uses httplib2 and BeautifulSoup to parse the UCLA dining page, checking if FEAST has flan.
Joke version of my riot skin scraper script.
This code is licensed under MIT creative license.
'''

#!/usr/bin/env python
import httplib2
from BeautifulSoup import BeautifulSoup

class PageNotFound(RuntimeError): pass


class FlanScraper(object):
	def __init__(self, url="http://menu.ha.ucla.edu/foodpro/", timeout=15):
		self.url, self.timeout = url, int(timeout)

	def fetch_Flans(self):
		http = httplib2.Http(timeout=self.timeout)
		headers, content = http.request(self.url)

		if not headers.get('status') == '200':
			raise PageNotFound("Could not fetch page from '%s'. Got %s." % (self.url, headers['status']))

		return content

	def parse_Flans(self, content):
		soup = BeautifulSoup(content)
		# print soup
		raw = soup.findAll("a" , { "class" : "menuloclink" })
		processed = []
		for line in raw:
			if len(line.contents[0]) < 15:
				continue
			if not line.contents[0] == "FEAST at Rieber":
				continue
			processed.append(str(line['href']))
		return processed
		# return processed

	def get_Flans(self):
		content = self.fetch_Flans()
		return self.parse_Flans(content)

		
	def fetch_Flanpage(self, url):
		http = httplib2.Http(timeout=self.timeout)
		headers, content = http.request('http://menu.ha.ucla.edu/foodpro/'+url)

		if not headers.get('status') == '200':
			raise PageNotFound("Could not fetch page from '%s'. Got %s." % ('http://menu.ha.ucla.edu/foodpro/'+url, headers['status']))

		return content
		
	def parse_Flanpage(self, content):
		soup = BeautifulSoup(content)
		raw = soup.findAll("li", { "class" : "level2"})

		for line in raw:
			# print line.find('a').contents[0]
			if len(line.find('a').contents[0]) < 12:
				continue
			if line.find('a').contents[0] == "Caramel Flan":
				return "there is flan today"
		
		# print "there is no flan today"
		return "there is no flan today"
		
	def get_Flanpage(self, url):
		content = self.fetch_Flanpage(url)
		return self.parse_Flanpage(content)
		
	def processFlans(self): 
		urls = self.get_Flans()
		prepend = ''
		
		for url in urls:
			print self.get_Flanpage(url)
			prepend = prepend + '\n'
		with file('theresflantoday.txt', 'r') as original: data = original.read()
		with file('theresflantoday.txt', 'w') as modified: modified.write(prepend + data)

			
if __name__ == '__main__':
	scraper = FlanScraper()
	# releases = scraper.get_Flans()
	scraper.processFlans()