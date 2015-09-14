########################################
# filter by name lenth and
# mayer, ambassor, princess, at, on... (not yet)
# recover family name
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import time as tm
import re

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
