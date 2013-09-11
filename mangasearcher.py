from os       import makedirs
from bs4      import BeautifulSoup
from urllib   import urlretrieve
from urllib2  import urlopen
from os.path  import exists, isfile
import mechanize
import cookielib
import re
import sys
import json

class Crawler:

  def __init__(self, url, chapter):
    self.url = url
    self.main_html = urlopen(url)
    self.main_soup = BeautifulSoup(self.main_html.read())
    self.chapter = chapter

  def scrape_page(self):
    curr_url = self.url
    url_split = curr_url.split('/')
    url_split_cnt = len(url_split)
    url_split_last = url_split[-1]

    curr_base_url_split = url_split[0:-1]
    curr_base_url = "/".join(curr_base_url_split)

    while (self.main_html.code == 200) and (url_split_last != ""):
    #if self.main_html.code == 200:
      img_src = self.get_image(self.main_soup)
      dir_name = self.create_dir(curr_url)
      self.downloadManga(img_src,dir_name)
      next_link = curr_base_url + '/' + self.get_next_link(curr_url)
      curr_url = next_link
      url_split = curr_url.split('/')
      url_split_last = url_split[-1]
      self.main_html = urlopen(curr_url)
      self.main_soup = BeautifulSoup(self.main_html.read())
      print url_split_last

  def get_next_chapter(self, url):
    url_split = url.split('/')
    base_url_split = url_split[0:-1]
    base_url = "/".join(base_url_split)

    next_chapter_num = int(url.split('/')[-2][1:4]) + 1
    next_chapter_link = base_url
    print next_chapter_link

  def get_next_link(self,url):
    next_html = urlopen(url)
    next_soup = BeautifulSoup(next_html.read())
    next_link = next_soup.find('a', {'class':'next_page'})
    return next_link.get('href')

  def create_dir(self, url):
    url_split = url.split('/')
    dir_name = url_split[-4] + '_' + url_split[-2]
    return dir_name

  def get_image(self, data):
    viewer = data.find(id='viewer')
    img = viewer.find('img')
    return img.get('src')

  def downloadManga(self,img_src,dir_name):

    dir_path = 'downloads/' + dir_name
    file_name = img_src.split('/')[-1]

    if not exists(dir_path):
      makedirs(dir_path)

    if not isfile(dir_path + '/' + file_name):
      try: 
        br = mechanize.Browser()

        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        image_response = br.open_novisit(img_src)

        with open(dir_path + '/' + file_name, 'wb') as f:
          f.write(image_response.read())
          print('Downloading ' + file_name + '...')

      except:
        print('Download error!')
    else:
      print('Image already exists.')

  def find_chapter(self):
    search_string = "Hajime no Ippo" + " " + str(self.chapter)
    result = self.main_soup.find_all('a', text=re.compile(search_string))
    return result[-1].get('href')

def main(argv):
  
  manga_url = 'http://mangafox.me/manga/'
  search_url = 'http://mangafox.me/ajax/search.php?term='
  search_string = argv[0]

  search_html = urlopen(search_url + search_string)
  bs = json.loads(search_html.read())

  cnt = 1
  for b in bs:
    print str(cnt) + ": " + b[1]
    cnt += 1

  user_choose = raw_input("Enter number to download: ")

  choosen_manga = bs[int(user_choose) - 1]

  choosen_manga_url = manga_url + choosen_manga[2]

  choosen_manga_title = choosen_manga[1]

  chapter = raw_input("Enter " + choosen_manga[1] + " chapter to download: ")
  end = raw_input("until: ")

  main_html = urlopen(choosen_manga_url)
  b = BeautifulSoup(main_html.read())

  try:

    for x in range(int(chapter), int(end)+1):
      print x
      search_string = choosen_manga_title + " " + str(x)
      chapter_link = b.find_all('a', text=re.compile(search_string))
      url = chapter_link[-1].get('href')
      print url

      c = Crawler(url,chapter)
      c.scrape_page()
  except:
    print "Sorry but an error has occured. Please try again later."

if __name__ == '__main__':
  main(sys.argv[1:])