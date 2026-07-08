# Task 1：Parse hotel data from internet and save to CSV files

import urllib.request as request
import json
import csv

with request.urlopen("https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch") as responseCH:
    dataCH = json.load(responseCH)

with request.urlopen("https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en") as responseEN:
    dataEN = json.load(responseEN)

# 英文名：'hotel name'
# 英文地址：'address'
# hotels.csv 中文data："旅宿名稱", "地址", "電話或手機號碼", "房間數"
# districts.csv：
# DistrictName："地址"第4~6個字元
# HotelCount：分類district後計算每個district的旅館數
# RoomCount："房間數"

# hotels.csv
hotelsListCH = dataCH["list"]
hotelsListEN = dataEN["list"]

# 需要透過"_id"比對並取得hotelsListCH和hotelListEN中相同旅館的資料
# 把hotelsListEN做成字典, key: _id, value: {"hotelName":"hn", "addressEN":"addr"}
hotelsDict = {}
for hotel in hotelsListEN:
    hotelsDict[hotel['_id']] = {"hotelNameEN":hotel["hotel name"], "addressEN":hotel["address"]}

# 把hotelsListCH的資料也加入字典
for hotel in hotelsListCH:
    hotelsDict[hotel["_id"]].update({"hotelNameCH":hotel["旅宿名稱"], "addressCH":hotel["地址"], "phone":hotel["電話或手機號碼"], "roomCount":hotel["房間數"]})
    # 處理district並加入hotelsDict中
    hotelsDict[hotel["_id"]].update({"district":hotel["地址"][3:6]})

# 寫入hotels.csv
with open("./week 3/hotels.csv", 'w', newline="", encoding="utf-8") as fileHotels:
    writer = csv.DictWriter(fileHotels, fieldnames=["hotelNameCH", "hotelNameEN", "addressCH", "addressEN", "phone", "roomCount"], extrasaction="ignore")

    for hotel in hotelsDict.values():
        writer.writerow(hotel)

# districts.csv

# 建立districts的字典key: district, value: {"districtName":"dn", "hotelCount":hc, "roomCount":rc}
districtsDict = {}
for hotel in hotelsDict.values():
    if hotel["district"] not in districtsDict:
        districtsDict[hotel["district"]] = {"districtName":hotel["district"]}

    if "hotelCount" in districtsDict[hotel["district"]]:
        districtsDict[hotel["district"]]["hotelCount"] += 1
    else:
        districtsDict[hotel["district"]].update({"hotelCount":1})

    if "roomCount" in districtsDict[hotel["district"]]:
        districtsDict[hotel["district"]]["roomCount"] += int(hotel["roomCount"])
    else:
        districtsDict[hotel["district"]].update({"roomCount":int(hotel["roomCount"])})

# 寫入districts.csv
with open("./week 3/districts.csv", 'w', newline="", encoding="utf-8") as fileDistricts:
    writer = csv.DictWriter(fileDistricts, fieldnames=["districtName", "hotelCount", "roomCount"], extrasaction="ignore")

    for district in districtsDict.values():
        writer.writerow(district)


# Task 2：Parse web page data and save to files by Python
from bs4 import BeautifulSoup
import urllib.parse as parse

INDEXPAGE = "https://www.ptt.cc/bbs/Steam/index.html"
MAINPAGE = "https://www.ptt.cc"

# 用beautifulsoup取得網頁html資料
def fetchHTML(url):
    with request.urlopen(url) as response:
        webpageContext = response.read().decode("utf-8")
        htmlContext = BeautifulSoup(webpageContext, "html.parser")
    return htmlContext

# 將html文章列表資料中取出文章標題、推、文章連結
def parseIndexHTML(html):
    articles = html.select("div.r-ent")
    articlesList = []

    for article in articles:
        titleTag = article.select_one("div.title a")
        nrecTag = article.select_one("div.nrec")

        title = titleTag.get_text(strip=True) if titleTag else "已刪文"
        href = titleTag.get("href") if titleTag else ""
        fullUrl = parse.urljoin(MAINPAGE, href)
        nrec = nrecTag.get_text(strip=True) if nrecTag else ""
        
        if title == "已刪文":
            continue
        elif nrec == "":
            nrec = "0"
        articlesList.append({"title":title, "nrec":nrec, "url":fullUrl})
    return articlesList

# 取得上頁url
def getPreviousPageUrl(html):
    prevPageUrl = html.find("a", string="‹ 上頁")

    if prevPageUrl:
        href = prevPageUrl["href"]
        fullUrl = parse.urljoin(MAINPAGE, href)
        return fullUrl
    else:
        return None
    
# 取得文章發文時間
def parseTime(url):
    articlePageHTML = fetchHTML(url)
    label = articlePageHTML.find("span", string="時間")
    time = label.findNextSibling("span").get_text(strip=True) if label else ""
    if time:
        return time
    else:
        return ""

# 重複執行上頁並取得文章資料三次
indexPageHTML = fetchHTML(INDEXPAGE)
articles = []
for i in range(3):
    articles= articles+parseIndexHTML(indexPageHTML)
    if i < 2:
        prevUrl = getPreviousPageUrl(indexPageHTML)
        if prevUrl is None:
            break
        indexPageHTML = fetchHTML(prevUrl)

# 把時間加到article的字典中
for article in articles:
    article["time"] = parseTime(article["url"])

# 寫入articles.csv
with open("./week 3/articles.csv", 'w', newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "time", "nrec"], extrasaction="ignore")

    for article in articles:
        writer.writerow(article)