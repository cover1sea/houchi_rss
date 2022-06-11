import time
import pprint
import xml.dom.minidom
from xml.dom.minidom import parseString
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def debug_msg(msg):
  if not __debug__:
    print(msg)

def get_info_from_web():
  options = Options()
  options.add_argument('--headless')
  driver = webdriver.Chrome(chrome_options=options)
  # or driver = webdriver.Chrome("path/to/webdriver")
  driver.get("https://hcsj.c4connect.co.jp/home")
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
    link = "https://hcsj.c4connect.co.jp/home"
    desc = item.find_element(
        By.CSS_SELECTOR, ".news-content .news-content-cell").get_attribute('innerHTML')
    data = {
        "news_no": news_no,
        "title": title,
        "date": date,
        "desc": desc,
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
  for data in datas:
      item = dom.createElement("item")
      channel.appendChild(item)

      title = dom.createElement("title")
      title.appendChild(dom.createTextNode(data["title"]))
      item.appendChild(title)

      date = dom.createElement("pubDate")
      date.appendChild(dom.createTextNode(data["date"]))
      item.appendChild(date)

      desc = dom.createElement("description")
      desc.appendChild(dom.createTextNode(data["desc"]))
      item.appendChild(desc)
  return dom.toprettyxml()


def main():
  datas = get_info_from_web()
  debug_msg(datas)
  debug_msg("+-----+")  
  
  rss_xml = create_rss(datas)
  debug_msg(rss_xml)

  return rss_xml 
  
if __name__ == '__main__':
  main()