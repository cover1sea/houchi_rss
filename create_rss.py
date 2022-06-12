#python -m pip install tzdata
#python -m pip install selenium
import time
import datetime
from zoneinfo import ZoneInfo
from email import utils
from xml.dom.minidom import parseString
import zoneinfo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

url_houchi_d = "https://hcsj.c4connect.co.jp/"
url_houchi_news = "https://hcsj.c4connect.co.jp/home"

def debug_msg(msg):
  if not __debug__:
    print(msg)

def create_rss_from_c4g():
  datas = get_info_from_web()
  debug_msg(datas)
  debug_msg("+-----+")  
  
  rss_xml = create_rss(datas)
  debug_msg(rss_xml)

  return rss_xml 

def get_info_from_web():
  options = Options()
  options.add_argument('--headless')
  driver = webdriver.Chrome(chrome_options=options)
  # or driver = webdriver.Chrome("path/to/webdriver")
  driver.get(url_houchi_news)
  time.sleep(2)
  list = driver.find_elements(
      By.CSS_SELECTOR, ".news-right-all .news-1 .news-content-cell")
  news_no_list = []
  for item in list:
      news_id = item.get_attribute("class")
      id_prefix = "s2-n-"
      idx = news_id.find(id_prefix)
      news_no = news_id[idx+len(id_prefix):]
      news_no_list.append(news_no)
  list = driver.find_elements(By.CSS_SELECTOR, ".modal-body .news-det")
  datas = []
  for item in list:
    news_id = item.get_attribute("class")
    id_prefix = "news-det-"
    idx = news_id.find(id_prefix)
    news_no = news_id[idx+len(id_prefix):]
    flag = False
    for i in news_no_list:
      if i == news_no:
        flag = True
        break
    if flag == False:
      continue
    title = item.find_element(
        By.CSS_SELECTOR, ".news-top .news-header").get_attribute('innerText')
    date = item.find_element(
        By.CSS_SELECTOR, ".news-top .news-date").get_attribute('innerText')
    link = url_houchi_news
    desc = item.find_element(
        By.CSS_SELECTOR, ".news-content .news-content-cell").get_attribute('innerHTML')
    desc_rep = desc.replace(r"../../", url_houchi_d)
    data = {
        "news_no": news_no,
        "title": title,
        "date": date,
        "desc": desc_rep,
        "url": link,
    }
    datas.append(data)
  driver.quit()
  datas_sorted = sorted(datas, key=lambda x: x["date"], reverse=True)
  return datas_sorted
  
def create_rss(datas):
  xml_template = "<rss version=\"2.0\">\
      <channel>\
          <title>放置少女 更新情報</title>\
          <link>https://hcsj.c4connect.co.jp/home</link>\
          <description>放置少女 更新情報</description>\
          <language>ja</language>\
      </channel></rss>"
  dom = parseString(xml_template)
  channel = dom.getElementsByTagName("channel")[0]

  now_rfc822 = iso8601_to_rfc822(datetime.datetime.now(ZoneInfo("Asia/Tokyo")))
  t = dom.createElement("lastBuildDate")
  t.appendChild(dom.createTextNode(str(now_rfc822)))
  channel.appendChild(t)

  for data in datas:
      item = dom.createElement("item")
      channel.appendChild(item)
      
      num = dom.createElement("guid")
      num.appendChild(dom.createTextNode(url_houchi_news+"#"+data["news_no"]))#dummy
      item.appendChild(num)

      title = dom.createElement("title")
      title.appendChild(dom.createTextNode(data["title"]))
      item.appendChild(title)

      date = dom.createElement("pubDate")
      d = date_to_rfc822(data["date"])
      date.appendChild(dom.createTextNode(str(d)))
      item.appendChild(date)

      desc = dom.createElement("description")
      desc.appendChild(dom.createTextNode(data["desc"]))
      item.appendChild(desc)
  return dom.toprettyxml()

def date_to_rfc822(date):
  date_l = date.split("/")
  date_8601 = datetime.datetime(int(date_l[0]), int(date_l[1]), int(date_l[2]), 20, 0, 0, 0, ZoneInfo("Asia/Tokyo"))
  return iso8601_to_rfc822(date_8601)

def iso8601_to_rfc822(d):
  return utils.formatdate(time.mktime(d.timetuple()), localtime=True)


def main():
  create_rss_from_c4g()
if __name__ == '__main__':
  main()