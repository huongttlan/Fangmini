import requests, re
import pandas as pd
import networkx as nx
from datetime import datetime
from bs4 import BeautifulSoup

# generate the urls for requested parties
url_base = 'http://www.newyorksocialdiary.com'
i = 0
urls = []
while True:
    response = requests.get(url_base+'/party-pictures', params={"page":i})
    soup = BeautifulSoup(response.text)
    parent_div = soup.find('div', attrs={'class':'view-content'})
    if parent_div == None:
        break
    date_divs = parent_div.find_all('span', attrs={'class':'views-field views-field-created'})
    url_divs = parent_div.find_all('a')
    for j in range(len(date_divs)):
        if datetime.strptime(date_divs[j].text.strip(), '%A, %B %d, %Y') < datetime(2014, 12, 1):
            urls.append(url_base+url_divs[j]['href'])
    i += 1

# extract all the captions
caw_captions = []
for i, url in urls[261:]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    parent_div = soup.find(attrs={'class':'field__item even'})
    caption_divs = parent_div.find_all(attrs={'class':'photocaption'})
    if len(caption_divs) < 5:
        caption_divs = parent_div.find_all(attrs={'size':'1'})
    for caption_div in caption_divs:
        if caption_div.text:
            raw_captions.append(caption_div.text.strip().encode('utf-8'))

# cut out long captions
captions = []
for caption in raw_captions:
    caption = re.sub(' +', ' ', caption.replace('\n','')) # remove blanks and \n in captions
    if len(caption) < 100: # remove long captions
        captions.append(caption)
print len(captions)

# add family name
def add_family_name(names):
    for i in range(len(names)-1):
        if ' ' not in names[i] and ' ' in names[i+1]:
            names[i] = names[i] + ' ' + names[i+1].split(' ')[-1]
    return names

# give pairs of names in one caption
def give_pairs(names):
    l = len(names)
    pairs = []
    for i in range(l):
        for j in range(l):
            if j > i:
                if names[i] < names[j]:
                    pairs.append((names[i], names[j]))
                else:
                    pairs.append((names[j], names[i]))
    return pairs

# remove false names
def remove_false_names(names):
    false_names = ['', 'friend','friends', 'a friend','MD','M.D.','Jr.',\
                   'his wife', 'children', 'guest', 'guests','family']
    new_names = []
    for name in names:
        if name not in false_names:
            new_names.append(name)
    return new_names

# extract names and pairs
all_names = []
all_pairs = []
for caption in captions:
    if ' and ' in caption or ' with ' in caption:
        caption = caption.replace(' and ', ' , ').replace(' with ',' , ')
        names = caption.split(',')
        names = [name.strip() for name in names]
        names = remove_false_names(names)
        names = add_family_name(names)
        # given a list of 'names' generated from one caption
        for name in names:
            all_names.append(name)
        for pair in give_pairs(names):
            all_pairs.append(pair)
all_names = list(set(all_names))
all_unique_pairs = list(set(all_pairs))

# analyze data using Graph
G = nx.Graph()
G.add_nodes_from(all_names)
G.add_edges_from(all_unique_pairs)

mydf1 = pd.DataFrame({'name':G.degree().keys(), 'degree':G.degree().values()})
mydf1 = mydf1.sort('degree', ascending=False)
mydf1[:100].describe()
names = list(mydf1['name'])
degrees = list(mydf1['degree'])
result1 = []
for i in range(100):
    result1.append((names[i], degrees[i]))
# answer to the first question

pr = nx.pagerank(G, alpha=0.85)
mydf2 = pd.DataFrame({'name':pr.keys(), 'pr':pr.values()})
mydf2 = mydf2.sort('pr', ascending=False)
mydf2[:100].describe()
names = list(mydf2['name'])
degrees = list(mydf2['pr'])
result2 = []
for i in range(100):
    result2.append((names[i], degrees[i]))
# answer to the second question

mydf3 = pd.DataFrame({'pair':all_pairs,'number':1})
by_pair = mydf3.groupby('pair').sum().sort('number', ascending=False)['number']
by_pair[:100].describe()
pairs = list(by_pair.index)
counts = list(by_pair)
result3 = []
for i in range(100):
    result3.append((pairs[i], counts[i]))
# answer to the third question
