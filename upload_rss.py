import ftplib
import create_rss

def debug_msg(msg):
  if not __debug__:
    print(msg)

def ftp_upload(host, port, user, password, file_path):
  debug_msg("FTP Connect "+host)
  with ftplib.FTP() as ftp:
    ftp.connect(host=host)#, port=port)
    ftp.set_pasv('true')
    debug_msg("FTP Login "+user)
    ftp.login(user, password)
    
    with open("houchi_news.xml", mode="rb") as f:
      debug_msg("FTP Upload :"+"STOR "+file_path+"houchi_news.xml")
      ftp.storbinary("STOR "+file_path+"houchi_news.xml", f)

def main():
  xml = create_rss.create_rss_from_c4g()
  
  debug_msg(xml)
  
  
  with open("houchi_news.xml", mode="w", encoding="utf-8") as f:
    f.write(xml)
  
  with open("ftp_account.dat", encoding="utf-8") as f:
    data = f.readline()
  datas = data.split(";")
  debug_msg(datas)
  ftp_upload(datas[0],int(datas[1]),datas[2],datas[3],datas[4])
  
if __name__ == '__main__':
  main()