import requests
import urllib.request
import bs4
import sys
import os


def create_path_if(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def main():
    print("enter the adresses of the mange :")
    adresse = input().split('//')[1]
    if adresse[-1] == '/' :
        adresse = adresse[:-1]
    mangaN = adresse.split('/')[-1] + '/'
    create_path_if(mangaN)
    #create adresse directory if he doesnt exist
    res = requests.get("http://m." + adresse)
    mangaS = bs4.BeautifulSoup(res.text, "lxml")
    elems = mangaS.select('dd[class="chlist"] a[href]')

    volume = elems[0]["href"].split('/')[-2]
    if (volume + '/') == mangaN :
        num = -2
    else :
        num = -3

    chlist = []
    for i in elems :
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

    for ch in chlist[beg:(end + 1)] :
        st = "http://m.mangafox.la/roll_manga/" + mangaN + ch + "/1.html"
        res = requests.get(st)
        soup = bs4.BeautifulSoup(res.text, "lxml")
        images = soup.select('img[class="reader-page"]')
        print(st)
        for b, mage in enumerate(images) :
            image = mage['data-original']
            path = (mangaN + ''.join(ch.split('/')) + '-' + str(b) + '.'
                        + image.split('?')[0].split('.')[-1])
            print(path)
            urllib.request.urlretrieve(image, path)

if (__name__ == "__main__"):
    main()
