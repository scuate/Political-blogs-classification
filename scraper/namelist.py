##get the name list of republican and liberal congress members/presidential candidates in 2011/2012
import yaml
import codecs
import re

def crtList(filename):
    f = open(filename,'r')
    doc = yaml.load(f)
    party = {'DEM':[],'GOP':[]}
    for person in doc:
        last_name = person['name']['last']
        first_name = re.split('[^A-Za-z]+',person['id']['wikipedia'])[0]
        for tm in person['terms']:
            start = int(tm['start'].split('-')[0])
            end = int(tm['end'].split('-')[0])
            if 2011 in range(start,end+1) or 2012 in range(start,end+1):
                p = tm['party'] 
                if p in party:
                    party[p].append((first_name,last_name))
                break
    return party

def crtHistList(filename,party_dict):
    f = open(filename,'r')
    doc = yaml.load(f)
    for person in doc:
        last_name = person['name']['last']
        first_name = person['name']['first']
        for tm in person['terms']:
            start = int(tm['start'].split('-')[0])
            if start < 1985:
                break
            end = int(tm['end'].split('-')[0])
            if 2011 in range(start,end+1) or 2012 in range(start,end+1):
                p = tm['party'] 
                if p in party:
                    party[p].append((first_name,last_name))
                break
    return party

def writeList(filename,party_dict):
    outfile = codecs.open(filename, 'wt', encoding='utf-8')
    num = 0
    for k in party_dict.keys():
        outfile.write('##'+k+'\n')
        for person in party_dict[k]:
            num += 1
            outfile.write(' '.join(person)+'\n')
    print 'person_num',num
    outfile.close()
    
def main():
    party_dict = crtList('legislators-current.yaml')
    party_dict2 = crtHistList('legislators-historical.yaml',party_dict)
    writeList('../data/congress',party_dict2)

main()