##extract the list of 2012 presidential candidates from the two wiki pages.

from bs4 import BeautifulSoup
import urllib2 
import codecs

def getGopCandidate(soup):
    candidates = []
    table = soup.find_all('table', class_='wikitable')
    table1 = table[0]
    btags = table1.find_all('b')
    for bt in btags:
        atext = bt.find(lambda tag:tag.name=='a' and tag.has_attr('href') and tag.has_attr('title') and not tag.has_attr('class'))
        if atext:
            name = atext.get_text()
            candidates.append(name)
    for t in table[1:]:
         ctrs = t.find_all('center')
         for c in ctrs:
             name = c.get_text()
             candidates.append(name)
    gallery = soup.find_all('div', class_= 'gallerytext')
    for g in gallery:
        name = g.p.b.get_text()
        candidates.append(name)
        
    return candidates

def getDemCandidate(soup):
    candidates = []
    table = soup.find_all('table', class_='wikitable')
    for t in table:
        btags = t.find_all('b')
        for bt in btags:
            name = bt.get_text()
            candidates.append(name)
    gallery = soup.find_all('div', class_= 'gallerytext')
    for g in gallery:
        name = g.p.b.get_text()
        candidates.append(name)
    return candidates

def writeCandidate(fname,label,candidates):
    outfile = codecs.open(fname,'at',encoding='utf-8')
    outfile.write('##'+label+'\n')
    for person in candidates:
        outfile.write(person+'\n')
    outfile.close()

def main():
    page1 = urllib2.urlopen('https://en.wikipedia.org/wiki/Republican_Party_presidential_candidates,_2012')
    soup1 = BeautifulSoup(page1)
    goplst = getGopCandidate(soup1)
    writeCandidate('../data/candidates','GOP',goplst)
    page2 = urllib2.urlopen('https://en.wikipedia.org/wiki/Democratic_Party_presidential_candidates,_2012')
    soup2 = BeautifulSoup(page2)
    demlst = getDemCandidate(soup2)
    writeCandidate('../data/candidates','DEM',demlst)

main()