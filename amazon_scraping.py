#!/usr/bin/python
# -*- coding: utf-8 -*-

# /*
#  * Copyright (c) Saverio Serravezza.
#  * All rights reserved.
#  * Content: [..]
#  * PYTHON version 2.7
#  * @copyright Saverio Serravezza
#  */


import _config
from lxml import html
from lxml.etree import tostring
import csv,os,json
import requests
from exceptions import ValueError
from time import sleep
import re
import random
from random import randint
from lxml.html import fromstring
from interruptingcow import timeout


### configuration
asinlist =['B001B4S4E8','B07NPLL29C','B002TDT14W','B003E36V2G']
locurl = "http://www.amazon.it/dp/"
### configuration



##### GET PROXIES #####
def get_proxies():
	try:
		url = 'https://free-proxy-list.net/'
		response = requests.get(url)
		parser = fromstring(response.text)
		proxies = []
		for i in parser.xpath('//tbody/tr')[:100]:
			if i.xpath('.//td[7][contains(text(),"yes")]'):
				proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
				proxies.append(proxy)
		print 'Proxies list acquired'
		return proxies
	except:
		print "Impossible to scrape proxy list, using local list"
		proxies = ['1.179.188.169','1.179.143.53','185.130.144.207','156.239.18.128','156.239.22.200','156.239.22.196','156.239.18.101','156.239.18.42','156.239.16.185','156.239.18.2','156.239.18.32','156.239.18.14','186.211.110.21','156.239.14.17','156.239.22.208','156.239.22.207','156.239.22.173','103.36.126.229','156.239.18.11','156.239.18.57','156.239.16.228','156.239.16.164','156.239.18.200','156.239.18.142','156.239.22.202','156.239.18.135','156.239.22.198','156.239.18.235','156.239.22.189','188.121.103.157','37.139.85.66','119.82.253.90','1.179.206.161','197.98.180.248','58.65.128.234','159.203.118.239','94.230.148.153','118.175.240.205','192.99.70.52','118.175.176.132','190.214.11.50','157.230.249.208','118.174.65.118','82.100.63.181','178.128.151.27','93.99.104.121','117.196.236.219','165.22.14.234','154.66.154.131','54.36.162.223','45.234.95.95','170.239.87.103','142.93.40.115','35.198.22.102','95.167.143.11','178.128.162.70','177.206.28.121','156.239.16.191','156.239.18.8','156.239.18.20','156.239.16.209','156.239.16.153','156.239.18.58','156.239.18.145','156.239.16.55','156.239.16.229','156.239.16.193','156.239.16.218','156.239.16.158','156.239.17.183','156.239.18.59','156.239.18.157','156.239.18.55','156.239.22.203','156.239.16.205','156.239.16.220','156.239.16.178','156.239.16.155','156.239.17.201','168.235.93.28']
		return proxies

##### PARSER FUNC #####
def AmzonParser(url):
	nretr = 0
	proxies = get_proxies()
	while True:
		sleep(randint(6, 12))
		if nretr > 26:
			sleep(30)
			proxies = get_proxies()
			nretr = 0
		print '#nretr ', nretr, ' - ',url
		useragent = random.choice(_config.useragents)
		headers = {'User-Agent': useragent}
		proxy = random.choice(proxies)
		print '..trying with proxy ',proxy, ' and useragent ',useragent[:40]
		try:
			with timeout(12):
				responsecheckstatus = None
				responsecheck = None
				try:
					responsecheck = requests.get('https://httpbin.org/ip',proxies={"http": proxy, "https": proxy})
					print responsecheck.json()
				except:
					print '- proxy connection Error with ', proxy
					responsecheckstatus = 1
					nretr = nretr +1
					continue
			with timeout(20):
				if responsecheckstatus != 1:
					print '- connection with proxy OK, proceeding '
					print '- processing: '+url+ ' with IP ',proxy
					try:
						page = requests.get(url,headers=headers,proxies={"http": proxy, "https": proxy})
						print 'Got page!'
					except:
						print 'Request Page not worked'
						nretr = nretr +1
						continue


					doc = html.fromstring(page.content)

					raw_name = doc.xpath('//h1[@id="title"]//text()')
					raw_images = doc.xpath('//script[contains(., "ImageBlockATF")]//text()')
					raw_brand = doc.xpath('//a[@id="bylineInfo"]//text()')
					raw_sizeweight = doc.xpath('//div[@class="attrG"]//div[@class="pdTab"]//*//tr[@class="size-weight"]//text()')
					raw_description = doc.xpath('//div[@id="productDescription"]//text()')
					raw_specifications = doc.xpath('//div[@class="column col1 "]//div[@class="section techD"]//div[@class="content pdClearfix"]//div[@class="attrG"]//div[@class="pdTab"]//table//text()')
					raw_category = doc.xpath('//div[@id="wayfinding-breadcrumbs_container"]//*//a[@class="a-link-normal"]//text()')
					raw_taglia = doc.xpath('//div[@id="variation_size_name"]//*//span[@class="selection"]//text()')
					raw_colore = doc.xpath('//div[@id="variation_color_name"]//*//span[@class="selection"]//text()')


					## preparing data
					name = 					' '.join(''.join(raw_name).split()) if raw_name else None
					brand = 				' '.join(' - '.join(raw_brand).split()).strip() if raw_brand else None
					sizeweight = 			' '.join(' - '.join(raw_sizeweight).split()).strip() if raw_sizeweight else None
					description = 			' '.join(''.join(raw_description).split()).strip().replace('\n', '') if raw_description else None
					category = 				' || '.join([i.strip() for i in raw_category]) if raw_category else None
					taglia = 				' '.join(''.join(raw_taglia).split()) if raw_taglia else None
					colore = 				' '.join(''.join(raw_colore).split()) if raw_colore else None


					## check if page content (name) is parsed
					if name != None:
						print 'Got Content!'
					else:
						raise ValueError('Request Content not found')
						nretr = nretr +1
						continue





					### images
					images = []
					if raw_images:
						raw_images_str = str(raw_images[0])
						raw_imagesext=raw_images_str[raw_images_str.find("'colorImages': ")+15:raw_images_str.find('}]},')]
						result_images = raw_imagesext+'}]}'
						result_imagesjson = json.loads(result_images.replace("'", '"'))
						for img in result_imagesjson['initial']:
							if img['hiRes'] == None or img['hiRes'] == '':
								images.append(img['large'])
							else:
								images.append(img['hiRes'])
					### images


					# specifications
					specifications = []
					num = 0
					for specs in raw_specifications:
						if specs.isspace()==False:
							num = num+1
							specifications.append(specs.strip())
							if (num % 2) != 0:
								specifications.append(': ')
							else:
								specifications.append('\n')
					specifications = ''.join(specifications) if specifications else None
					# specifications


					if page.status_code!=200:
						raise ValueError(' --- Errore del server ',page.status_code)


					#### print debugging
					print '-----------------'
					print ''
					print "NAME:::: ", name
					print ''
					print "ASIN:::: ", url.rsplit('/', 1)[-1]
					print ''
					print "CATEGORY:::: ",category
					print ''
					print "BRAND:::: ",brand
					print ''
					print "SIZE AND WEIGHT:::: ",sizeweight
					print ''
					print "IMAGES:::: ",images
					print ''
					print "DESCRIPTION:::: ",description
					print ''
					print "SPECIFICATION:::: ",specifications
					print ''
					print "TAGLIA:::: ",taglia
					print ''
					print "COLORE:::: ",colore
					print '-----------------'
					print ''
					#### print debugging



					data = {
							'name':name,
							'asin':url.rsplit('/', 1)[-1],
							'url':url,
							'category':category,
							'brand':brand,
							'sizeweight':sizeweight,
							'images':images,
							'description':description,
							'specifications':specifications,
							'taglia':taglia,
							'colore':colore,
							}
					return data

		except Exception as e:
			print '-- Error ',e
			continue


##### SCRAPING list of Asins
extracted_data = []
tries = 0
for asincode in asinlist:
	url = locurl+asincode
	extracted_data.append(AmzonParser(url))
	if extracted_data:
		f=open('data_scrap_amz.json','wa')
		json.dump(extracted_data,f,indent=4)
		tries = tries +1
		print '  >> Done  ##: ',tries, ' - Asin: ', asincode




## s.s. || eof ##
