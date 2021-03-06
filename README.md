# PWCC_Crawler
This is a web crawler for PWCC, which is the leader in the trading card investment marketplace. 

Today my target is this card：[2003 lebron rc topps chrome refractor psa](https://reurl.cc/XWeqQg).

My mission is to grab all the information in this site data like picture link, sold card name, sold price etc all we can saw the useful information. Than, sort out this data to the total price of years run chart.

## Ordeal
The sold price is a difficult point for crawler in PWCC. In order to see the sold price, we must be logged in.

![alt text](https://raw.githubusercontent.com/ahoucbvtw/PWCC_Crawler/main/Picture/01.jpg "The problem of crawler in PWCC")

Before we log in, we must to know what kind of data we should to post in login process.

First, go to login page, press **```Ctrl+Shift+I```** to show the site of source code and go to 「Network」 page. Next, type casually to log in(Login failed is no problem), then find the request method is **「POST」** login headers in 「Network」 page.

*ps. **```Ctrl+Shift+I```** is useful in **Chrome** to open source code page. Please find how to open source code page in your browser.*

![alt text](https://raw.githubusercontent.com/ahoucbvtw/PWCC_Crawler/main/Picture/02.jpg "Request method POST of login page")

Second, go down the headers can see the 「Form Data」 column. The column of data is we should post in login process.

![alt text](https://raw.githubusercontent.com/ahoucbvtw/PWCC_Crawler/main/Picture/03.jpg "Necessary of log in data")

As we can see, **「_token」** is a random word. Thus, before login, I turn to **「Element」** page to find where is the _token is it and write down the code.

![alt text](https://raw.githubusercontent.com/ahoucbvtw/PWCC_Crawler/main/Picture/08.jpg "The _token random word")

**To catch 「_token」  code：**

**```csrftoken = soupresult.find("meta",{"name":"csrf-token"}).get('content')```**
 
 *ps. If anyone who want to see the source code when login success, login fail and after login price, I also upload these three html files in this repository.*
 
 ## Result
 
 This is all of data in is this card：[2003 lebron rc topps chrome refractor psa](https://reurl.cc/XWeqQg), and I was built the Table below.
 
 ![alt text](https://raw.githubusercontent.com/ahoucbvtw/PWCC_Crawler/main/Picture/05.jpg "The table of crawled data")
   
 Here is the total price of years run chart.
  
 ![alt text](https://raw.githubusercontent.com/ahoucbvtw/PWCC_Crawler/main/Picture/07.png "The total price of run chart")
