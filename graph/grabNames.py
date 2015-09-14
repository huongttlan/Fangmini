########################################
# filter by name lenth and
# mayer, ambassor, princess, at, on... (not yet)
# recover family name
########################################
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import time as tm
import re

raw_captiondf = pd.DataFrame(columns=('event_url', 'event_date', 'photocaption'))
for pg in range(26):
    raw_captiondf = raw_captiondf.append(pd.read_pickle('Page' + str(pg)), ignore_index=True)

print 'Raw_caption: ', len(raw_captiondf)

# filter by date "cre_date"
cre_date = datetime.strptime('12/01/2014', "%m/%d/%Y")
date_captiondf = raw_captiondf[raw_captiondf.event_date < cre_date]
print 'After filter by date', cre_date, 'caption number is: ', len(date_captiondf)

# filter by date "cre_cutoff = 250 characters"
cre_cutoff = 250;
short_captiondf = date_captiondf[date_captiondf.apply(lambda row:len(row['photocaption']), axis=1) < cre_cutoff]
print 'After filter by caption length ', cre_date, ' characters, caption number is: ', len(short_captiondf)


caption0 = pd.DataFrame(short_captiondf.photocaption).reset_index(drop=True)
caption0['names']=''
caption0['num_names']=''
caption0.head()


def findName(cption):
    cption = re.sub(",\s+and", ", ", cption )
    cption = re.sub("\swith\s", ", ", cption)
    cption = re.sub("\s+and\s", ", ", cption)
    cption = re.sub("\s&\s", ", ", cption)
    name = re.split(',\s', cption)
    return [nm.strip() for nm in name]

for i in caption0.index:
    caption0.names[i] = findName(caption0.photocaption[i])
    caption0.num_names[i] = len(caption0.names[i])

# one word is not a human name
caption1 = caption0[caption0.num_names>1]
caption1.to_pickle('caption1')

##############################################
# second round filter

caption1 = pd.read_pickle('caption1').reset_index('drop=Ture')
#should iterate over all names

for k in caption1.index:
    print k
    names = caption1.names[k]
    print names
    for name in range(len(names))[::-1]:
#        print name
#        print names[name]
        if len(re.findall(r'\w+', names[name])) > 4:
            del names[name]
            continue
            
        if names[name] in ['Dr.', 'M.D.', 'Ph.D.']:
            del names[name]
            continue
        names[name] = re.sub("Dr. ", "", names[name])
        
        if len(re.findall(r'\w+', names[name])) == 1:
            if name == len(names)-1:
                del names[name]
            else:
                names[name] = names[name] + ' ' +re.findall(r'\w+', names[name+1])[-1]
    print names
    caption1.num_names[k] = len(names)
#    print caption1.num_names[k]
caption2 = caption1
caption2 = caption2[caption2.num_names>1]
caption2.to_pickle('caption2')
