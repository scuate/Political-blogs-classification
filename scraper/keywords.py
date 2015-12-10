##extract the keywords of each party from the html pages, remove the common words from both parties
from bs4 import BeautifulSoup
import urllib
import re


def getKeywords(soup):
    keywords = []
    labels = soup.find_all('a',class_='g-node')
    for l in labels:
        keyword_raw = l['xlink:href'].lower()
        keyword = re.sub('%20',' ',keyword_raw[1:])
        if '%2f' in keyword:
            words = keyword.split()
            w1 = words[0]
            w2 = words[-1]
            keywords.extend([w1,w2])
        else:
            keywords.append(keyword)
    return keywords

def rmCommonWords(gopLst,demLst):
    gopSet = set(gopLst)
    demSet = set(demLst)
    common = gopSet.intersection(demSet)
    gopLst = list(gopSet.difference(common))
    demLst = list(demSet.difference(common))
    gopLst.sort()
    demLst.sort()
    return (gopLst,demLst)

def writeKeywords(fname,gopLst,demLst):
    outfile = open(fname,'w')
    outfile.write('##GOP\n')
    for w in gopLst:
        outfile.write(w+'\n')
    outfile.write('##DEM\n')
    for w in demLst:
        outfile.write(w+'\n')
    outfile.close()

def main():
    page1 = urllib.urlopen('gopWords.html')
    soup1 = BeautifulSoup(page1)
    gopLst = getKeywords(soup1)
    page2 = urllib.urlopen('demWords.html')
    soup2 = BeautifulSoup(page2)
    demLst = getKeywords(soup2)
    gop_wordlst, dem_wordlst = rmCommonWords(gopLst,demLst)
    writeKeywords('../data/keywords',gop_wordlst,dem_wordlst)

main()