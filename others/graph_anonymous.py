### Scrape web pages ###

import urllib2
import datetime
import re
from collections import namedtuple
from bs4 import BeautifulSoup

def crawl_nysocial():
    """ Return a list of events info
    """
    # Store events name, url, time in PartyInfo
    PartyInfo = namedtuple('PartyInfo', 'title url time')

    def party_info(td):
        """ Return namedtuple with event info
        Input: td - BeautifulSoup instance
        """
        content = td.select('span.views-field')
        event_title = content[0].find('a').text
        party_url = content[0].find('a')['href']
        t = datetime.datetime.strptime(content[1].text, ' %A, %B %d, %Y ')
        party_time = datetime.date(t.year, t.month, t.day)
        if party_time < datetime.date(2014, 12, 1):
            return PartyInfo(title=event_title,
                             url=party_url,
                             time=party_time)
        else:
            return None

    def crawl(url):
        """ Return all events info on the url
        Input: url - str
        """
        raw_page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(raw_page)
        event_divs = soup.select('div.view-content div.views-row')
        event_links = [party_info(td) for td in event_divs
                       if party_info(td) is not None]
        return event_links

    # Get all events info
    url = "http://www.newyorksocialdiary.com/party-pictures"
    all_events = []
    for i in xrange(1, 26):  # loop through page 1 to 25
        new_url = url + '?page=' + str(i)
        all_events.extend(crawl(new_url))
    return all_events


def get_captions(party_info):
    """ Return captions for all events
    Input: party_info - namedtuple that contains all events information
    """
    url_base = "http://www.newyorksocialdiary.com"
    try:
        soup = BeautifulSoup(urllib2.urlopen(url_base + party_info.url))
        # Rules for scraping captions
        captions = soup.select('div.photocaption')
        captions = captions + soup.select('tr td.photocaption')
        captions = captions + soup.select('div font')

        selected_captions = []
        for i in xrange(len(captions)):
            text = captions[i].text
            # td.photocaption rule may grab nested tags
            # Add the following rule to avoid duplicates
            m = re.match('^\n', text)
            if not m and text != '':
                selected_captions.append(text)
        return selected_captions
    except:
        print 'HTTP error'  # 503 error
        return None

# Get all events information
all_parties = crawl_nysocial()
print len(all_parties)

# Get all captions
all_captions = []
counter = 1

for i in xrange(len(all_parties)):
    print counter
    caption = get_captions(all_parties[i])
    if caption is None:
        caption = get_captions(all_parties[i])
    else:
        all_captions.extend(caption)
    counter += 1

print len(all_captions)

# Write all captions into ny_social_captions.txt
f = open('ny_social_captions.txt', 'wb')
for caption in all_captions:
    m = re.match(r'^ ?Photographs ', caption)
    if not m: # Not adding photographer names
        # Remove redundant whitespaces
        caption = re.sub(' +', ' ', caption.replace('\n', ''))
        f.write("%s\n" % caption.encode('utf8'))
f.close()


########################### parsing ###############################
### Parsing all captions and create .csv files for submission ###

import re
import operator
import numpy as np
import networkx as nx

# Read captions file
f = open('./ny_social_captions_smaller.txt', 'rb')
all_captions = list(f)

# Code is getting slow as number of nodes/edges are getting large...
# Split caption into 6 partitions
split_index = np.linspace(0, len(all_captions), num=7, dtype=int)[1:-1]
graph_dict = dict([(num, nx.Graph()) for num in range(6)])


counter = 1
# Loop through 6 partitions of caption list
for i in range(len(split_index)+1):

    # Set start and end index for each partition
    if i == 0: start = 0
    else: start = split_index[i-1]

    if i == len(split_index): end = len(all_captions) + 1
    else: end = split_index[i]
    
    for caption in all_captions[start:end]:
        print 'Graph #', i
        print 'Caption #:', counter

        # Only look at cpations with length < 250
        if len(caption) < 250:    
            # Parsing rules
            rm_prefix = re.compile('(\)|\?|Jr|Dr|Mr|Mrs|Ph\.?D|M\.?D)\W', re.I)
            caption = rm_prefix.sub('', caption)
            caption = re.sub(r'\n', ' ', caption)
            caption = re.sub(r'a? friends?', '', caption)
            caption = re.sub(r'sons?', '', caption)
            caption = re.sub(r'daughters?', '', caption)
            caption = re.sub(r'family', '', caption)

            # Create list of names appearing in one caption
            names = [s.strip() for s in re.split(r'\Wand\W|,|\Wwith\W|\Wat\W',
                                                 caption, flags=re.IGNORECASE)
                     if s.strip()]

            # Take care of special cases...
            for name in names:
                if 'Mayor' in name and 'Bloomberg' in name:
                    name = 'Michael Bloomberg'
                if 'President' in name and 'Clinton' in name:
                    name = 'Bill Clinton'

            # Add family name for "Jane and John Doe" cases
            if len(names) == 2 and len(names[0].split()) == 1:
                names[0] = names[0] + ' ' + ' '.join(names[1].split()[1:])

            names.sort()
            # Add all name nodes
            graph_dict[i].add_nodes_from(names)
            
            # Add an edge for each pair in the caption
            for index, name in enumerate(names):
                for other in names[index+1:]:
                    try:  # if edge exists
                        graph_dict[i][name][other]['weight'] += 1
                    except:  # add new edge
                        graph_dict[i].add_weighted_edges_from([(name, other, 1)])

            print len(graph_dict[i].nodes())
            print len(graph_dict[i].edges())

        counter += 1

# Merge all graphs into one
G = nx.Graph()

for i in range(len(graph_dict)):
    G.add_nodes_from(graph_dict[i])
    for (n1, n2) in graph_dict[i].edges():
        try:
            G[n1][n2]['weight'] += graph_dict[i][n1][n2]['weight']
        except:
            G.add_weighted_edges_from([(n1, n2, 
                                        graph_dict[i][n1][n2]['weight'])])


### Question 1 - degree ###
all_degree = {}
for n, nbrs in G.adjacency_iter():
    degree = 0
    for nbr, eattr in nbrs.items():
        degree = degree + eattr['weight']
    all_degree[n] = degree

# Get the top 100 nodes with high degree
sorted_degree = sorted(all_degree.items(), key=operator.itemgetter(1))
top_100_degree = sorted_degree[-100:]
top_100_degree.reverse()

# Save result and will read it from __init__.py for submission
g = open('./degree.csv', 'wb')
for node in top_100_degree:
    line = node[0] + ',' + str(node[1])
    g.write(line)
    g.write('\n')
g.close()


### Question 2 - pagerank ###

pg = nx.pagerank(G, alpha=0.85)
sorted_pg = sorted(pg.items(), key=operator.itemgetter(1))

# Remove invalid names
valid_pg = []
for rank in sorted_pg[::-1]:
    if len(rank[0].split()) >= 2:
        valid_pg.append(rank)
top_100_pg = valid_pg[:100]

g = open('./pagerank.csv', 'wb')
for node in top_100_pg:
    line = node[0] + ',' + str(node[1])
    g.write(line)
    g.write('\n')
g.close()


### Question 3 - best friends ###

# Sort edges by weight
sorted_friends = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
top_100_friends = sorted_friends[-100:]
top_100_friends.reverse()

g = open('./friends.csv', 'wb')
for node in top_100_friends:
    line = node[0] + ',' + node[1] + ',' + str(node[2]['weight'])
    g.write(line)
    g.write('\n')
g.close()
