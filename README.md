Manga Searcher
======================

A python script which lets you search and download any manga that you want.

Requirements:
  * <a href="http://www.python.org/getit/">Python 2.7+</a>
  * <a href="http://www.crummy.com/software/BeautifulSoup/#Download">BeautifulSoup 4</a>
  * <a href="http://wwwsearch.sourceforge.net/mechanize/">Mechanize</a>

Currently supports:
http://mangafox.me

Usage:

Run:
```bash
$ python mangasearcher.py "MANGA_TITLE_HERE"
```

Example:
```bash
$ python mangasearcher.py "Hajime no ippo"

1: Hajime no Ippo
2: Hajime
3: Hajime-chan ga Ichiban!
4: Change!
5: Nemureru Mori
6: Kiss Kara Hajime You
7: Hima na no de Hajime de Mimasu

Enter number to download: 1
Enter Hajime no Ippo chapter to download: 1
until: 5

1
http://mangafox.me/manga/hajime_no_ippo/v01/c001/1.html
Downloading ippo_vol_01_000.jpg...
2.html
Downloading ippo_vol_01_003.jpg...
3.html
...
...
...
```

It will download the manga to the downloads folder as shown below.

![alt tag](https://raw.github.com/lucentx/mangasearcher/master/images/download_folder.png)
![alt tag](https://raw.github.com/lucentx/mangasearcher/master/images/download_files.png)