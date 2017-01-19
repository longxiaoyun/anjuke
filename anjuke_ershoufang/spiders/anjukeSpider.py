# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import logging
from anjuke_ershoufang.items import AnjukeErshoufangItem
import re

from bs4 import  BeautifulSoup

# 设置编码格式  
import sys
reload(sys)  
sys.setdefaultencoding('utf-8')

logger = logging.getLogger("anjuke spider")

class anjukeSpider(CrawlSpider):
	
	name="anjuke"
	allowed_domains=["shanghai.anjuke.com"]


	website_possible_httpstatus_list=[403]
	handle_httpstatus_list=[403]

	start_urls=["http://shanghai.anjuke.com/sale/?from=navigation"]



	# 获取每个区的url
	def parse(self,response):
		if response.body=="banned":
			req=response.request
			req.meta["change_proxy"]=True
			yield req
		else:

			item=AnjukeErshoufangItem()

			soup=BeautifulSoup(response.body,'lxml')
			# 获取大区的链接
			name=soup.find('div',{'class':'items'}).find('span',{'class':'elems-l'}).find('a').get_text()

			print name

			item['region']=name

			urls=soup.find('div',{'class':'items'}).find('span',{'class':'elems-l'}).find('a').get('href')
			print 'urls========================>',urls

			yield Request(urls,callback=self.parse_item,meta={'item':item})

			# for region in urls:

			# 	print 'region========>',region

			# 	if region is not None:
			# 		# print 'region------===>',region

			# 		yield Request(region,callback=self.parse_item)




			# yield response.reques


	def parse_item(self,response):

		# item=AnjukeErshoufangItem()
		item = response.meta['item']

		# 下一页
		soup=BeautifulSoup(response.body,'lxml')
		next_link=soup.find('div',{'class':'sale-left'}).find('div',{'class':'multi-page'}).find('a',{'class':'aNxt'})

		# sub_next_link=next_link.find('div',{'class':'multi-page'})

		# next_href=sub_next_link.find('a',{'class':'aNxt'}).get('href')
		if next_link is not None:
			
			next_href=next_link.get('href')
			yield Request(next_href,callback=self.parse_item,meta={'item':item})


		# print 'next_href---------------------->',next_href


		# yield Request(next_href,callback=self.parse_item,meta={'item':item})







		# item
		ul=soup.find_all('ul',{'id':'houselist-mod'})

		for li in ul:

			div=li.find('div',{'class':'house-details'})

			a=div.find('a',{'class':'houseListTitle'}).get('href')

			# print 'a=========================>',a

			if a is not None:

				yield Request(a,callback=self.parse_info,meta={'item':item})




	# 获取页面内房源详细信息
	def parse_info(self,response):
		# item=LianjiaItem()
		item = response.meta['item']

		reg=re.compile('\s+')

		soup=BeautifulSoup(response.body,'lxml')




		item['url']=response.request.url

		# print 'this url is:************************',response.request.url

		totalPrice=soup.find('div',{'class':'basic-info clearfix'}).find('span',{'class':'light info-tag'}).get_text()

		# print 'totalPrice==========>',totalPrice

		item['totalPrice']=totalPrice


		# 户型图
		houseTypeImg=soup.find('div',{'id':'hx_pic_wrap'}).find('div',{'class':'img_wrap'}).find('img').get('src')
		item['houseTypeImg']=houseTypeImg





		houseInfo=soup.find('div',{'class':'houseInfoV2-detail clearfix'})
		if houseInfo is not None:
			first=houseInfo.find('div',{'class':'first-col detail-col'})
			second=houseInfo.find('div',{'class':'second-col detail-col'})
			third=houseInfo.find('div',{'class':'third-col detail-col'})
			if first is not None:
				dl=[dl.text for dl in first.find_all('dl')]

				court=re.sub(reg,'',dl[0])
				# print 'court===================>',court
				item['court']=court

				address=re.sub(reg,'',dl[1])
				# print 'address======================>',address
				item['address']=address

				age=re.sub(reg,'',dl[2])
				# print 'age======================>',age
				item['age']=age

				houseType=re.sub(reg,'',dl[3])
				# print 'houseType=======================>',houseType
				item['houseType']=houseType

			if second is not None:

				dl=[dl.text for dl in second.find_all('dl')]

				roomType=re.sub(reg,'',dl[0])
				# print 'roomType=====================>',roomType
				item['roomType']=roomType

				area=re.sub(reg,'',dl[1])
				# print 'area========================>',area
				item['area']=area

				forward=re.sub(reg,'',dl[2])
				# print 'forward===================>',forward
				item['forward']=forward

				floor=re.sub(reg,'',dl[3])
				# print 'floor=================>',floor
				item['floor']=floor
			if third is not None:
				dl=[dl.text for dl in third.find_all('dl')]

				decoration=re.sub(reg,'',dl[0])
				# print 'decoration===================>',decoration
				item['decoration']=decoration

				unitPrice=re.sub(reg,'',dl[1])
				# print 'unitPrice====================>',unitPrice
				item['unitPrice']=unitPrice

				downPayment=re.sub(reg,'',dl[2])
				# print 'downPayment========================>',downPayment
				item['downPayment']=downPayment

				monthlyPayment=re.sub(reg,'',dl[3])
				# print 'monthlyPayment====================>',monthlyPayment
				item['monthlyPayment']=monthlyPayment




		# 上次交易
		item['lastTrade']='null'


		# 房屋年限
		item['houseTimelimit']='null'



		yield item






