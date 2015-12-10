##reads in external source data, store data in a dictionary to be used by proc_file.py

from sys import argv
import math

##reads in two files-congress and candidates,combine the data into one dict {lastname:[(firstname,party)]}
class partyMembers():
    def __init__(self,fname1,fname2):
        self.dict = {}
        self.crtDict(fname1,self.dict)
        self.crtDict(fname2,self.dict)
        
    
    def addPersonParty(self,line,label,dict):
        lst = line.split()
        last = lst[-1].lower()
        first = lst[0].lower()
        if last not in dict:
            dict[last] = [(first,label)]
        else:
            exist = False
            for fn,l in dict[last]:
                if fn == first:
                    exist == True
                    break
            if not exist:
                dict[last].append((first,label))

    def crtDict(self,fname,dict):
        f = open(fname)
        line = f.readline().rstrip()
        while not line:
            line = f.readline().rstrip()
        if '##' in line:
            idx = line.rfind('#')
            label = line[idx+1:]
        line = f.readline().rstrip()
        while '##' not in line:
            self.addPersonParty(line,label,self.dict)
            line = f.readline().rstrip()
        idx = line.rfind('#')
        label = line[idx+1:]
        line = f.readline().rstrip()
        while line:
            self.addPersonParty(line,label,self.dict)
            line = f.readline().rstrip()
    
    def getDict(self):
        return self.dict

#reads in the keywords file, store "keyword:party" pairs in a dict
class partyKeywords():
    def __init__(self,fname):
        self.dict = {}
        self.crtDict(fname,self.dict)
    
    def addKeywordParty(self,line,label,dict):
        if line not in dict:
            dict[line] = label

    def crtDict(self,fname,dict):
        f = open(fname,'r')
        line = f.readline().rstrip()
        while not line:
            line = f.readline().rstrip()
        if '##' in line:
            idx = line.rfind('#')
            label = line[idx+1:]
        line = f.readline().rstrip()
        while '##' not in line:
            self.addKeywordParty(line,label,self.dict)
            line = f.readline().rstrip()
        idx = line.rfind('#')
        label = line[idx+1:]
        line = f.readline().rstrip()
        while line:
            self.addKeywordParty(line,label,self.dict)
            line = f.readline().rstrip()

    def getDict(self):
        return self.dict
