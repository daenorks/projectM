#!/usr/bin/python3

import requests
import urllib.request
import bs4
import sys
import os
import time


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def main():
    adresse = ' '.join(sys.argv[1:])
    mangaN = adresse.split('/')[-2] + '/'
    assure_path_exists(mangaN)
    #create adresse directory if he doesnt exist
    res = requests.get(adresse)
    mangaS = bs4.BeautifulSoup(res.text, "lxml")
    elems = mangaS.select('a[class="tips"]')

    chlist = []
    for i in elems :
        num = -3
        if (i["href"].split('/')[-3] + '/') == mangaN :
            num = -2
        chlist.append("/".join(i['href'].split('/')[num:-1]))
    chlist = chlist[::-1]
    #create directory for each volume
    for i, b in enumerate(chlist) :
        print(i, b)
    # select chapter
    print("enter the number of the first chapter you want to download :")
    beg = int(input())
    print("enter the number of the last chapter you want to download: ")
    end = int(input())

    for i in chlist[beg:(end + 1)] :
        res = requests.get(adresse + i + "/1.html")
        print(adresse + i + "/1.html")
        soup = bs4.BeautifulSoup(res.text, "lxml")
        s = soup.select('div .l')
        mpage = int(str(s[0]).split()[-2])
        print(i)
        for b in range(1, mpage + 1) :
            while (True):
                res = requests.get(adresse + i + "/" + str(b) + ".html")
                soup = bs4.BeautifulSoup(res.text, "lxml")
                image = soup.select("#image")[0]['src']
                path = (mangaN + '/' + ''.join(i.split('/')) + '-' + str(b) +
                    '.' + image.split('?')[0].split('.')[-1])
                try :
                    urllib.request.urlretrieve(image, path)
                except urllib.error.HTTPError:
                    pass
                if os.path.isfile(path) :
                    break
            print(b)

if (__name__ == "__main__"):
    main()
