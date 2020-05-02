import os
import time
import json
import random

import requests
import bs4
from requests_oauthlib import OAuth1Session

class Watcher:
	def __init__(self, url, productname):
		self.url = url
		self.pname = productname
		self.now = self.time_to_txt()
		self.lasttime = time.localtime()
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
		self.target_price = 0
		self.price = 1e9
		self.pprice = 0
		self.bot = Twitter()

	def show_price(self):
		self.pprice = self.price
		res, raw, price = self.get_price()
		txt = self.now
		txt += ' : '
		if res == False: txt += 'Error!'
		elif price == 1e9 or price != self.target_price: 
			self.price = 1e9
			txt += '在庫切れ'
			if self.price != self.pprice:
				self.bot.send(self.pname + ' は現在在庫切れです. \n' + self.url)
		else:
			self.price = price
			txt += raw
			if self.price != self.pprice:
				self.bot.send(self.pname + ' は現在' + raw + 'で販売中です. \n購入はお早めに！\n' + self.url)
		print(txt)

	def get_price(self):
		res = requests.get(self.url, headers=self.headers)
		soup = bs4.BeautifulSoup(res.text, features="lxml")
		availability = soup.select('#availability span.a-size-medium')
		if availability == []: return False, '', 0
		status = availability[0].text.replace(' ', '').replace('\n', '')
		if status == '現在在庫切れです。': return True, status, 1e9
		price = soup.select('span.a-color-price')
		if price == []: return False, '', 0
		return True, price[0].text, int(price[0].text[1:].replace(',', ''))

	def time_to_txt(self, tm=[]):
		if tm == []: tm = time.localtime()
		res = ''
		res += self.add_zero(tm[1]) + '月'
		res += self.add_zero(tm[2]) + '日 '
		res += self.add_zero(tm[3]) + ':'
		res += self.add_zero(tm[4]) + ':'
		res += self.add_zero(tm[5])
		return res

	def add_zero(self, num):
		if (num) >= 10: return str(num)
		else: return '0'+str(num)

	def timer(self):
		base = 30
		mn = -10
		mx = 10
		nexttime = self.set_nexttime(base, mn, mx)
		while (1):
			tm = time.localtime()
			if tm[4] - self.lasttime[4] >= 2: nexttime = self.set_nexttime(base, mn, mx)
			if tm[5] == nexttime and tm[4] != self.lasttime[4]:
				nexttime = self.set_nexttime(base, mn, mx)
				self.lasttime = tm
				self.now = self.time_to_txt(tm)
				self.show_price()

	def set_nexttime(self, base, mn, mx):
		return base + random.randint(mn, mx)

class Twitter():
	def __init__(self):
		data = self.load_APIdata()
		self.bot = OAuth1Session(data['CLIENT_KEY'], data['CLIENT_SECRET'], data['RESOURCE_OWNER_KEY'], data['RESOURCE_OWNER_SECRET'])

	def load_APIdata(self):
		fname = os.path.join(os.path.dirname(__file__), 'APIkey.json')
		data = json.load(open(fname, 'r'))
		return data

	def send(self, msg):
		from http import HTTPStatus
		param = {'status': msg}
		res = self.bot.post('https://api.twitter.com/1.1/statuses/update.json', param)
		if res.status_code == HTTPStatus.OK:
			print('Tweet: ' + msg)
		else:
			print('Tweet failed. StatusCode: ' + str(res.status_code))

def main():
	url = 'https://www.amazon.co.jp/dp/B07QLRRQB3'
	productname = 'Oculus Rift S'
	a = Watcher(url, productname)
	a.target_price = 50722
	a.timer()

if __name__ == '__main__':
	main()