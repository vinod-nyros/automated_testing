import pyquery
import urllib2

url = "https://www.google.com/search?q=WD+Red+internal+drives&client=ubuntu&channel=fs&biw=1421&bih=843&noj=1&tbs=vw:l&tbm=shop&ei=0F_aVOGYJpSZoQTisIDwCw&ved=0COgDEL0N"
req = urllib2.Request (url, headers={ 'User-Agent': 'Mozilla/5.0' })
html = urllib2.urlopen(req).read()

print html
