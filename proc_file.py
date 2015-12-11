##reads in an individual file and paramLst(F1 through F6), process the file and create feature vector

from sys import argv
from outsource import partyMembers,partyKeywords
import re
import random


##for F5, count the keywords of each party in a doc
def cntKeyword(ngram,partyKeyword,F5):
    if ngram in partyKeyword:
        party = partyKeyword[ngram]
        F5[party] += 1

#go through the doc, extract ngrams(n=1,2,3) and count the keywords
def extractFeats(paramLst,F1,F2,F3,F5,lst,partyKeyword):
    F2on = paramLst[1]==1
    F3on = paramLst[2]==1
    F5on = paramLst[4]==1
    for i in range(len(lst)):
        w = lst[i]
        if w not in F1:
            F1[w] = 1
        else:
            F1[w] += 1
        if F5on:
            cntKeyword(w,partyKeyword,F5)
        if i < len(lst)-1:
            if i < len(lst)-2:
                if F3on or F5on:
                    tri = '_'.join(lst[i:i+3])
                    if F3on:
                        if tri not in F3:
                            F3[tri] = 1
                        else:
                            F3[tri] += 1
                    if F5on:
                        cntKeyword(tri,partyKeyword,F5)
            if F2on or F5on:
                bi = '_'.join(lst[i:i+2])
                if F2on:
                    if bi not in F2:
                        F2[bi] = 1
                    else:
                        F2[bi] += 1
                if F5on:
                    cntKeyword(bi,partyKeyword,F5)

##for F6, use (0.5+0.5*rawFreq/maxFreqinDoc) to avoid bias towards longer docs
def cmptRelativeFreq(ngramF):
    if ngramF != {}:
        i = 0
        maxFreq = None
        for k in sorted(ngramF,key=ngramF.get,reverse=True):
            if i == 0:
                maxFreq = ngramF[k]
            relFreq = 0.5 + 0.5*ngramF[k]/maxFreq
            ngramF[k] = round(relFreq,2)
            i += 1

#for F4,count the person names from each party--search by last name, if there're > 1 first names, check the prev word, if prev word not a name, decide the party label randomly
def cntPerson(count,lst,partyMember):
    for i in range(len(lst)):
        w = lst[i]
        if w in partyMember:
            flst = partyMember[w]
            if len(flst) == 1:
                party = flst[0][1]
                count[party] += 1               
            else:
                wprev = lst[i-1]
                found = False
                for first,party in flst:
                    if wprev == first:
                        count[party] += 1
                        found = True
                        break
                if not found:
                    party = random.choice(flst)[1]
                    count[party] += 1

##for F4/F5,use rawMentionCnt/docWordCnt as the feature value to offset the large variance of doc length
def cmptMentionRt(count,wc):
    cntGOP = float(count['GOP'])
    cntDEM = float(count['DEM'])
    if wc!=0:
        count['GOP'] = round(cntGOP/wc,6)*100
        count['DEM'] = round(cntDEM/wc,6)*100


##go through the doc line by line, create features based on the paramLst
def crtFeature(paramLst,infile,partyMember,partyKeyword):
    f = open(infile,'r')
    F1 = {}
    F2 = {}
    F3 = {}
    F4cnt = {'GOP':0,'DEM':0}
    F5cnt = {'GOP':0,'DEM':0}
    F4on = paramLst[3]==1
    F6on = paramLst[5]==1
    feats = []
    line = f.readline()
    wc = 0
    while line:
        line = line.rstrip()
        if line:
            line = re.sub(r'[^0-9\-a-zA-Z]',' ',line).lower()
            lst = line.split()
            wc += len(lst)
            extractFeats(paramLst,F1,F2,F3,F5cnt,lst,partyKeyword)
            if F4on:
                cntPerson(F4cnt,lst,partyMember)                    
        line = f.readline()
    f.close()
    cmptMentionRt(F4cnt,wc)
    cmptMentionRt(F5cnt,wc)    
    F4 = {'gopPerson':F4cnt['GOP'],'demPerson':F4cnt['DEM']}
    F5 = {'gopKeyword':F5cnt['GOP'],'demKeyword':F5cnt['DEM']}

    ##finalizing features based on paramLst
    if F6on:
        for F in [F1,F2,F3]:
            cmptRelativeFreq(F)
    orig_feats = [F1,F2,F3,F4,F5]
    for i,st in enumerate(paramLst[:5]):
        if st == 1:
            feats.append(orig_feats[i])
    return feats

##write the output of feature-value pairs to the outfile
def writeFile(label,outfname,inp):
    outfile = open(outfname,'a')
    outfile.write(label+' ')
    for feature in inp:
        for k in sorted(feature):
            outfile.write(k+':'+str(feature[k])+' ')
    outfile.write('\n')
    outfile.close()

## create_vectors.py calls this function to process each file under a dir
def procFile(paramLst,infile,label,outfile):
    if paramLst[3] == 1: ##get the dict for F4
        partyMember = partyMembers('data/congress','data/candidates').getDict()
    else:
        partyMember = None
    if paramLst[4] == 1: ##get the dict for F5
        partyKeyword = partyKeywords('data/keywords').getDict()
    else:
        partyKeyword = None
    inp = crtFeature(paramLst,infile,partyMember,partyKeyword)
    writeFile(label,outfile,inp)

