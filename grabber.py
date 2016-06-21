
import urllib.request
import re
import datetime
import os
BING_URL = "http://www.bing.com"
import ctypes


if __name__ == "__main__":
    print(BING_URL)
    Bingpage = urllib.request.urlopen(BING_URL)
    imagepath = ""
    for line in Bingpage:
        #print(str(line))
        url = re.search(r'g_img={url:.+?"(.+?)"',str(line))
        if url:
            print(url.group(1))
            imagepath = url.group(1)
    temp = re.sub(r'\\+','',imagepath)
    photourl = BING_URL + temp
    photo = urllib.request.urlopen(photourl)
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    localphoto = open(year+'-'+month+'-'+day+'.jpg','wb')
    localphoto.write(photo.read())
    print(os.path.realpath(localphoto.name))
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0,os.path.realpath(localphoto.name) , 2)
    localphoto.close()
