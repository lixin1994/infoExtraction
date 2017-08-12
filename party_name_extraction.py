
'''
This is the previous RE:


((([A-Z][a-z]{2,8} \d{1,2}[A-Za-z]{0,2}, \d\d\d\d)|(\d{1,2}\w{1,2}? day of [A-Z][a-z]{2,8},? \d{4}))
,? \(.*Effective[^\)]*\))|(and ([A-Z][a-zA-Z&-]*,? ?)+&? (Co\.?|Inc\.?|Corporation|LLC|LLP|INC\.?))|((between|among)
 ([A-Z][a-zA-Z&-]*,? ?)+&? (Co\.?|Inc\.?|Corporation|LLC|LLP|INC\.?))
'''
import threading
import _thread
import re
import urllib
from bs4 import BeautifulSoup
import signal
import xlsxwriter

import csv

def download_file(url: str) -> str:
	'''
	Given: url that links to a certain website.
	Return: the content of this website.
	'''
	response = urllib.request.urlopen(url)
	content = response.read()

	return content


def urls_list(path: str) -> list:
	'''
	Given: the path of the file that has a lit of urls.
	Return: a list of urls
	'''
	url_file = open(path, mode='r')
	return url_file.readlines()

def process_html(file_content: str) -> str:
	'''
	Given: a raw html file
	Return: the paragraph of this contract that has the party names and date.
	'''
	soup = BeautifulSoup(file_content, 'html.parser')
	contract = soup.find('div', {'class': 'row contract-content'})
	content = contract.div.div
	return content.getText()

def get_party_names(paragraph_content: str, content_length: int) -> list:
	'''
	Given: a random paragraph
	Return: the party names of in this paragraph
	'''

	# list of possible enddings for party names
	shorten_list = ['LP','L\.P\.', 'L\.L\.C\.', 'LLC', 'LC', 'Ltd\.?', 'Co\., Inc\.', 'Ltd\.?', 'Co\.?( |,|\.)', 'Inc\.?', 'Corporation', 'LLP', 'L\.L\.P\.', 'INC\.?', 'PLC', 'P\.L\.C\.', 'GP', 'G\.P\.', 'DST', 'D\.S\.T\.','PC', 'P\.C\.', 'PLLC', 'P\.L\.L\.C\.', 'LLLP', 'L\.L\.L\.P\.', 'Trust', 'NA', 'N\.A\.', 'A\.G\.', 'AG']
	names = []
	paragraph_snippet = paragraph_content[0:content_length]

	# iterate each endding
	for shorten in shorten_list:
		name_temp = re.compile(r'([1-9A-Z][1-9a-zA-Z\.&]*,?&? )+' + shorten)
		search_result = name_temp.search(paragraph_snippet)
		start = 0
		while search_result:
			names.append(search_result.group(0))
			start = search_result.span()[1]
			paragraph_snippet = paragraph_snippet[start::]
			search_result = name_temp.search(paragraph_snippet)

	return names

def signal_handler(signum, frame):
    raise Exception("Timed out!")


def get_list_of_party_names(path: str, content_length: int) -> list:
	# Given the path and length of text that needs to be analyzed
	# Return the list party names
	url_list = urls_list(path)
	result_file = open('result.txt', 'w')
	k = 0
	p = 0
	workbook = xlsxwriter.Workbook('data.xlsx')
	worksheet = workbook.add_worksheet()
	row = 0
	for i in url_list:
		names = get_party_names(process_html(download_file(i)), content_length)
		col = 0
		for j in names:
			# Write into the excel file
			worksheet.write(row, col, j)
			col+=1
		worksheet.write(row, col, i)
		print(names)
		row+=1
	result_file.close()
	return [k,p]

def get_date(paragraph_content: str) -> str:


	pass
