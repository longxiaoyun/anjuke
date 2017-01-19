# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import json
import codecs
import re

class AnjukeErshoufangPipeline(object):

	def __init__(self):

		self.file=codecs.open('anjuke.json','w',encoding='utf-8')

	def process_item(self, item, spider):
		line=json.dumps(dict(item),ensure_ascii=False)+'\n'
		self.file.write(line)
		return item

	def spider_closed(self,spider):

		self.file.close()


def dbHandle():

	conn=MySQLdb.connect(
		host="",
		user="",
		passwd="",
		charset="utf8",
		db="houseInfo",
		use_unicode=False
		)
	
	return conn



class AnjukeMysqlPipeline(object):

	def process_item(self,item,spider):
		dbObject=dbHandle()
		cursor=dbObject.cursor()

		sql='INSERT INTO anjuke_ershoufang (url,totalPrice,roomType,area,unitPrice,age,decoration,forward,downPayment,monthlyPayment,court,address,\
			floor,lastTrade,houseType,houseTimeLimit,houseTypeImg,region) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		param=(item['url'],item['totalPrice'],item['roomType'],item['area'],item['unitPrice'],item['age'],item['decoration'],
				item['forward'],item['downPayment'],item['monthlyPayment'],item['court'],item['address'],item['floor'],item['lastTrade'],
				item['houseType'],item['houseTimelimit'],item['houseTypeImg'],item['region'])

		try:
			cursor.execute(sql,param)


			dbObject.commit()

			# print 'param=======>',param
		except Exception as e:
			print e
			dbObject.rollback()
		return item
