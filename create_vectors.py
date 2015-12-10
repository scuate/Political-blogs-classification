##reads in the dir names,get the paramLst(which features to use),call procFile to process each input file and output the file with feature vectors 

from sys import argv
from subprocess import Popen,PIPE
import optparse
from proc_file import procFile
import re

##call this script with the option '-f' will invoke the procFile module to process a single file
def readCommand(argv):
    parser = optparse.OptionParser()
    parser.set_defaults(procFile=False)
    parser.add_option('-f', action='store_true', dest='procFile', help='process an individual file')
    option,args = parser.parse_args(argv)
    return option,args

##get the params (which features to use) from the param file
def getParams(args):
    paramf = open(args[1],'r')
    param_lst = []
    for line in paramf:
        line = line.rstrip()
        param = line.split('=')
        param_lst.append(int(param[1]))
        
    paramf.close()
    return param_lst

    
##return a list of all the files under a dir (ls -ordered)
def listDir(path):
    p = Popen(('ls',path), shell=False,stdout=PIPE)
    return [fname.rstrip() for fname in p.stdout.readlines()]

    
##read in the dir names, process files and output to train_vector_file and test_vector_file
def procDir(args,paramLst):
    vector_f = args[2]
    dirlst = args[3:]
    for dir in dirlst:
        docs = listDir(dir)
        if dir[-1] != '/':
            idx_base = dir.rfind('/')
            label = dir[idx_base+1:]
        else:
            idx_base = dir[:-1].rfind('/')
            label = dir[idx_base+1:-1]
            dir = dir[:-1]
        num = 0
        for doc in docs:
            num += 1
            fname = dir+'/'+doc
            procFile(paramLst,fname,label,vector_f)
#        print 'docs',num
    
if __name__ == "__main__":
    option,args = readCommand(argv)
    paramLst = getParams(args)
    if option.procFile:  ##if '-f', process a single file
        procFile(paramLst,*args[2:]) #exclude paramfname from args
    else:  ##without '-f', process all files under given dirs
        procDir(args,paramLst)
