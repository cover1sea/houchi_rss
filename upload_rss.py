import ftplib
import create_rss

def ftp_upload(file):
  ftp = ftplib.FTP(IP_ADDRESS)
  ftp.set_pasv('true')
  ftp.login(USER, PASSWORD)

def main():
  xml = create_rss.create_rss_from_c4g()
  
  with open("houchi_news.xml", mode="w", encoding="utf-8") as f:
     f.write(xml)
  
  #ftp_upload(xml)
  
if __name__ == '__main__':
  main()