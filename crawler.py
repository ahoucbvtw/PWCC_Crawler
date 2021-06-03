import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse
import time
import numpy as np

def plot(dataframe): # 畫趨勢圖
	fig, ax = plt.subplots(figsize = (20, 10))

	ax.plot(dataframe["Total_Price"], "o-", label = "Price")
	ax.set_xticks(np.arange(len(dataframe["Year"])))
	ax.set_xticklabels(dataframe["Year"])

	for a,b in zip(dataframe.index, dataframe['Total_Price']):
		plt.text(a, b+5, '%.2f' % b, ha='center',fontsize=9)

	ax.legend()

	plt.xlabel("Year")
	plt.ylabel("Total_Price")
	plt.savefig("趨勢圖.png")
	print("趨勢圖.png已經儲存完畢！！")

def trand_data(dataframe): # 製作趨勢圖所需的資料並儲存CSV檔
	dataframe["SALE_DATE"] = dataframe["SALE_DATE"].apply(year) # SALE_DATE只取年份
	saleyear = dataframe["SALE_DATE"].value_counts().index.sort_values() # 獲取SALE_DATE中不重複且已經排序過的年份

	# 對SALE_DATE中一樣的年份進行統整分類
	frame_class = dataframe.groupby('SALE_DATE')

	# 計算排序好的各年份總價格
	totalmoney = []
	for i in saleyear:
		totalmoney.append(frame_class.get_group(i)["SOLD_PRICE"].sum())

	# 製作各年份的總價格CSV檔
	df = pd.DataFrame({'Year' : saleyear, 'Total_Price' : totalmoney})
	df.to_csv("趨勢圖.csv", index = False)
	print("\n趨勢圖.csv已經儲存完畢！！")

	return df

def year(text): # SALE_DATE只取年份
	return text[:4]

def fixtext(text):
	return text.replace(" ", "").replace("\n", "")

def text2float(text):
	return float(text.replace(",", ""))

def search(session, headers, page = 1, search = False): # 爬蟲
	nexturl = f"https://www.pwccmarketplace.com/market-price-research?items_per_page=50&price_max=10000&price_min=50&q=2003%20lebron%20rc%20%20topps%20chrome%20refractor%20psa&sale_type=auction&sort_by=date_desc&year_max=2021&year_min=2004&page={page}"

	response = session.get(nexturl, headers = headers)
	response.encoding = 'UTF-8' 

	soup = BeautifulSoup(response.text, 'html.parser')

	# 先確定是否要爬取資料還是爬取總頁數
	if search == True:
		date = []
		price = []
		picture = []
		item_name = []
		sale_type = []

		for text_picture in soup.find_all("td",{"class":"item-image"}):
			try:
				picture.append(text_picture.find("img",{"class":"img-fluid d-block mx-auto hover-scale"}).get('src'))
			except:
				picture.append(None)

		for text_itemname in soup.find_all("td",{"class":"card-title"}):
			item_name.append(text_itemname.getText().strip())

		for text_date in soup.find_all("td",{"class":"no-wrap"}):
			d = text_date.getText().split(":")[1].strip()
			date.append(datetime.strftime(parse(d), '%Y-%m-%d')) # 將"May 11, 2021"轉成"2021-05-22"

		for text_saletype in soup.find_all("span",string = "Sale Type:"):
			sale_type.append(fixtext(text_saletype.find_parents("td")[0].getText().strip()).split(":")[1])

		for text_price in soup.find_all("td",{"class":"item-price"}):
			price.append(text2float(text_price.getText().strip().replace("$", "")))

		return picture, item_name, date, sale_type, price

	else: # 只爬取總頁數
		text = soup.find("div",{"class":"col-md-6 text-center text-md-right"}).getText().replace(" ", "").replace("\n", "")
		page_count = int(text.split("of")[1].split("results")[0]) // int(text.split("of")[0].split("-")[1])
		allpages = page_count + 1 if page_count != 0 else page_count

		return allpages

if __name__ == '__main__':

	print("由於PWCC需要登入才能詳細知道卡片價位")
	print("因此請先於此進行登入\n")

	email = input("請輸入PWCC登入信箱：")
	password = input("請輸入PWCC登入密碼：")

	if email == "" or password == "":
		print("請輸入PWCC登入信箱 or 密碼！！")

	else:
		print("\n登入中請稍候...\n")

		url = "https://www.pwccmarketplace.com/login"
		session = requests.Session()

		# 查詢post所需的csrftoken
		tokenresult = session.get(url)
		tokenresult.encoding = 'UTF-8'
		soupresult = BeautifulSoup(tokenresult.text, 'html.parser')
		csrftoken = soupresult.find("meta",{"name":"csrf-token"}).get('content')

		headers={
			"accept-Language":"ja-JP,ja;q=0.9,zh-TW;q=0.8,zh;q=0.7,en-US;q=0.6,en;q=0.5",
			"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
			'referer': 'https://www.pwccmarketplace.com/login'
		}

		formdata = {
			"redirect":"",
			"email":email,
			"password":password,
			"remember":"1",
			"_token":csrftoken
		}

		# 登入
		response = session.post(url, headers = headers, data = formdata)

		# 判斷登入成功與否
		loginresult = BeautifulSoup(response.text, 'html.parser')
		login = loginresult.find("strong",string = "These credentials do not match our records.") # 此為輸入錯誤的登入資訊會出現的字

		if login == None: # 登入成功
			# 登入成功後搜尋UserName
			username = loginresult.find("div",{"class":"col-12 d-none d-sm-flex align-items-center pl-4"}).getText().strip()
			print(f"{username} 先生/小姐，目前您已經順利登入，準備開始查詢！！\n")

			# 第一輪先查詢總頁數
			totalpage = search(session, headers, page = 1, search = False)
			print(f"此次準備抓取頁數共 {totalpage} 頁\n")

			picture_link = []
			name = []
			date = []
			sale = []
			price = []

			# 抓取完整的爬蟲資料並儲存
			for i in range(totalpage):
				print(f"目前正在抓取page = {i + 1} 的資料，請稍候...")
				picturelink_, name_, date_, sale_, price_ = search(session, headers, page = i + 1, search = True)

				picture_link += picturelink_
				name += name_
				date += date_
				sale += sale_
				price += price_

				time.sleep(5)

			dataframe = pd.DataFrame({'PictureLink': picture_link,
									'SALE_ITEM': name,
									'SALE_DATE': date,
									'SALE_TYPE': sale,
									'SOLD_PRICE': price})

			# 儲存原始數據
			dataframe.to_csv("crawlerdata.csv", index = False)
			print("\n抓取的資料(crawlerdata.csv)已經儲存完畢！！")

			# 對數據進行轉換成年份對價格的趨勢圖資料
			df = trand_data(dataframe)

			# 畫年份對價格的趨勢圖
			plot(df)
		else:
			print("您輸入的信箱或密碼有誤，無法登入！！")