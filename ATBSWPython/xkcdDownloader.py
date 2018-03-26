#!/usr/local/bin/python

## Download all Xkcd.com comics
#

import requests, os, bs4, threading

url = 'http://xkcd.com'
os.makedirs('xkcd', exists_ok=True)

def downloadXkcd(startComic, endComic):
  for urlNumber in range(startComic, endComic):
      # Download the page
      print('Downloading page ... %s ' % (url))
      res = request.get(url)
      re.raise_for_status()
  
      soup = bs4.BeautifulSoup(res.text)
  
      # Find the url for the comic image
      comicElem = soup.select('#comic img')
      if comicElem == []:
          print('Could not find the comic element.')
      else:
          comicUrl = comicElem[0].get('src')
          # Download the image
          print('Downloading image ... %s' % (comicUrl))
          res = requests.get(comicUrl)
          res.raise_for_status()
  
      # Save the image to ./xkcd
      imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl), 'wb'))
      for chunk in res.iter_content(100000):
          imageFile.write(chunk)
      imageFile.close
  
      # Get the prev button's url.
      prevLink = soup.select('a[rel="prev"]')[0]
      url = 'http://xkcd.com' + prevLink.get('href')


downloadThreads = []

for i in range(0, 1400, 100):
  downloadThread = threading.Thread(target=downloadXkcd, args=(i, i+99))
  downloadThreads.append(downloadThread)
  downloadThread.start()

# Wait for all threads to finish:

for downloadthread in downloadThreads:
  downloadThread.join()
 
print('Done.')
