#!/usr/bin/python
# coding: utf8

import urllib2
from bs4 import BeautifulSoup
import csv

class Parties(object):
	def __init__(self, url):
		self.data = BeautifulSoup(urllib2.urlopen(url).read())
		self.http = "http://"
		self.parties = []
		self.parties_links = dict()

	def get_parties_names(self, attr_name, attr_val):
		for party in self.data.find_all(attrs={attr_name: attr_val}):
			self.parties.append(party.string)
		return self.parties

	def get_parties_links(self, attr_name, attr_val):
		for party in self.data.find_all(attrs={attr_name: attr_val}):
			self.parties_links[party.string] = self.http + "bechirot.gov.il/election/Candidates/Pages/" + party.a["href"]
		return self.parties_links


class Candidates:
	def __init__(self, url):
		self.data = BeautifulSoup(urllib2.urlopen(url).read())
		self.http = "http://"
		self.candidates = []

	def get_candidate_names(self, party, attr_name, attr_val):
		for name in self.data.find_all(attrs={attr_name: attr_val}):
			self.candidates.append(name.string)
		return self.candidates

	def write2file(self, file_name, party):
		with open(file_name, "ab") as csv_file:
			c = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
			num = 0
			for candidate in self.candidates:
				num += 1
				c.writerow([party.encode('utf-8'), candidate.encode('utf-8'), num])

def main():
	parties = Parties("http://bechirot.gov.il/election/Candidates/Pages/default.aspx")
	names = parties.get_parties_names("class", "candidates-title-k")
	links = parties.get_parties_links("class", "internallinkKnessetTitle")
	for party_name, link in links.iteritems():
		candidates = Candidates(link)
		party_candidates = candidates.get_candidate_names(party_name, "class", "candidate")
		candidates.write2file("candidates", party_name)


if __name__ == '__main__':
	main()

