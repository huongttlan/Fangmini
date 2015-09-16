# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 02:35:13 2015
@author: jacky ma
"""

#Change the Settings to decide the methods to run!
crawl_index=False
crawl_caption=False
parse_caption=True

#Code start here

#import networkx as nx
import sqlite3
import requests
import datetime
import string
import pandas as pd
from bs4 import BeautifulSoup
from collections import namedtuple
from lxml import etree
import lxml.html
import networkx as nx
import itertools

con = sqlite3.connect('GraphProject.db')
baseurl = 'http://www.newyorksocialdiary.com'
pageRecord = namedtuple('pageRecord', 'eventTitle, eventDate, eventHref')


def ExtractEventData(row):
#Extract a named tuple from a row given by soup.select('div.view-content div.views-row')
    eventHref=row.find('a')['href']
    eventTitle=row.find('a').text
    eventDate=datetime.datetime.strptime(row.find_all('span', class_='field-content')[1].text, '%A, %B %d, %Y')
    return pageRecord(eventTitle, eventDate, eventHref)
    
def ExtractIndexPage(url):
#Extract the rows from a page and call ExtractEventData to parse the rows
#Extract the link for next page if exist, return None if no next page    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    rows_div = soup.select('div.view-content div.views-row')
    next_link = soup.select('li.pager__item.pager__item--next a')
    next_link = next_link[0]['href'] if len(next_link)>0 else None
    return [ExtractEventData(row) for row in rows_div], next_link
    
def StartCrawling():
#Assign landpage, call ExtractIndexPage, repeat until no next page
#Write data to sqlite database, replace existing table
    print 'Start fetching pages...'    
    landingPage = '/party-pictures'
    data, nextlink = ExtractIndexPage(baseurl + landingPage)
    while nextlink is not None:
        print nextlink
        newdata, nextlink = ExtractIndexPage(baseurl + nextlink)
        data.extend(newdata)
    print 'End fetching pages...'
    df=pd.DataFrame(data)
    df.columns=['Title', 'Date', 'URL']
    df.index.name='pageid'
    df.to_sql('IndexPages', con, if_exists='replace', index_label='pageid')
    return df

def LoadIndexPageFromDB():
#Load data from DB, constrained to records before 2014-12-01
    print 'Load IndexPage URLs from DB'
    return pd.read_sql('SELECT * FROM IndexPages', con, index_col='pageid')

def ExtractPhotoCaption(url):
    response = requests.get(url)
    #soup = BeautifulSoup(response.text, "lxml")
    #photocaptions_div = soup.select('div.photocaption')
    #return [x.text for x in photocaptions_div]
    html = lxml.html.fromstring(response.text)
    photocaptions_div = html.xpath('//table[tr/td/img[contains(@src, "/partypictures/")]]//td[not(div[@class])] | //div[@class="photocaption"] | //td[@class="photocaption"] ')
    return [x.text_content().strip() for x in photocaptions_div if x.text_content().strip()!='']
 
def ExtractAllPhotoCaption(df):
    print 'Extract captions from pages...'
    data = []
    for pageid,row in df.iterrows():
        print 'Fetching ' + row.URL
        photocaptions = ExtractPhotoCaption(baseurl + row.URL)
        data.extend([(pageid, caption) for caption in photocaptions])
    df=pd.DataFrame(data)
    df.columns=['pageid', 'caption']
    df.index.name='captionid'
    df.to_sql('Captions', con, if_exists='replace', index_label='captionid')
    return df
    
def LoadPhotoCaptionFromDB():
    print 'Load Captions from DB'    
    return pd.read_sql('SELECT * FROM Captions', con, index_col='captionid')

def ClassifyCaption(inRow):
    stopwords=['Photographs by', 'Click here']
    removewords=['NYC', 'Board member', 'Young Professional', 'Committee', 'friend', 'friends', 'children', 'President', 'Kellogg', 'Guest', 'Front', 'row', 'family', 'Chair', 'Governor', 'MD', 'M.D.', 'Jr.', 'Ph.D.', 'Dr.', 'Mayor']
    replacewords=['with']

    inStr=inRow.caption
    textclass=0

    for word in stopwords:
        if inStr.find(word) >=0 : textclass=2

    for word in removewords:
        inStr=inStr.replace(word, '')
    
    for word in replacewords:
        inStr=inStr.replace(word, ',')
        
    totalCount = len(inStr)
    upperCaseCount = len(filter(lambda x: x in string.uppercase, inStr))
    lowerCaseCount = len(filter(lambda x: x in string.lowercase, inStr))
    termsCount = 1 + len(filter(lambda x: x == ',', inStr)) + (1 if 'and' in inStr else 0)
    avgTermLength = totalCount * 1.0 / termsCount 
    avgUCaseRatio = lowerCaseCount * 1.0 / (upperCaseCount + 0.001)
    avgTermUCase = upperCaseCount * 1.0 / termsCount 
    
    if textclass == 0:
        textclass = 1 if avgTermLength > 20 else 0
    return pd.Series({'pageid':inRow.pageid, 'caption': inStr, 'avgTermLength':avgTermLength, 'avgUCaseRatio':avgUCaseRatio ,'avgTermUCase':avgTermUCase, 'Class':textclass })

def CreateClassifyFields(df):
    print 'Classifying Captions (names / non-names)...'    
    return df.apply(ClassifyCaption, axis=1)

def ParseNames(captionSeries):
    print 'Parsing names in captions'
    data=[]
    for captionid,caption in captionSeries.iteritems():
        ppl = caption.split(',')
        for p in ppl:
            if ' and ' in p:
                names=p.split(' and ')
                if len(names)==2:
                    surname=names[1].split(' ')[-1]
                    #single word name
                    if ' ' not in names[0].strip(): names[0] = names[0].strip() + ' ' + surname
                ppl.remove(p)
                ppl.extend(names)
        #only names with two or more words is meaningful
        data.extend([(captionid, x.strip()) for x in ppl if ' ' in x.strip()])
    df=pd.DataFrame(data)
    df.columns=['captionid', 'person']
    df.index.name='PICid'
    df.to_sql('PersonInCaption', con, if_exists='replace', index_label='PICid')
    return df
    
def LoadPICFromDB():
    print 'Load Person In Captions from DB'    
    return pd.read_sql('SELECT * FROM PersonInCaption', con, index_col='PICid')

def ParseSocialNetwork(df):
    print 'Building network structure' 
    MG=nx.MultiGraph()
    dfg=df.groupby('captionid')
    for captionid, grp in dfg:
        ppl=grp.person
        edges = itertools.combinations(ppl, 2)
        MG.add_edges_from(edges)
    return MG

def MG_to_G(MG):
    G = nx.Graph()
    for u,v in MG.edges_iter():
        if G.has_edge(u,v):
            G[u][v]['weight'] += 1
        else:
            G.add_edge(u, v, weight=1)
    return G
    
def NodeDegree(g_socialnetwork):
    data=[]
    for n in g_socialnetwork.nodes():
        data.append((n, g_socialnetwork.degree(n, weight='weight')/2))
    sorteddata = sorted(data, key=lambda tup: tup[1], reverse=True)
    return sorteddata[:100]    
   
def NodePageRank(g_socialnetwork):
    d=nx.pagerank(g_socialnetwork, alpha=0.85, weight='weight')
    dl=[(key, value) for (key, value) in d.iteritems()]
    sortedlist = sorted(dl, key=lambda tup: tup[1], reverse=True)
    return sortedlist[:100]
    
def EdgeRank(nx_socialnetwork):
    e=nx_socialnetwork.edges(data=True)
    sorteddata =sorted(e, key=lambda tup:tup[2]['weight'], reverse=True)
    sorteddata = [((s[0], s[1]), s[2]['weight']) for s in sorteddata]
    return sorteddata[:100]
### Main Procedures


### Crawling
df_pages=StartCrawling() if crawl_index else LoadIndexPageFromDB()
df_caption=ExtractAllPhotoCaption(df_pages) if crawl_caption else LoadPhotoCaptionFromDB()

### Parsing
if parse_caption:
    df_caption_classified=CreateClassifyFields(df_caption)
    df_names_in_picture=ParseNames(df_caption_classified[(df_caption_classified.Class==0) & (df_caption_classified.pageid>80)]['caption'])
else:
    df_names_in_picture=LoadPICFromDB()

### Building Network    
mg_socialnetwork=ParseSocialNetwork(df_names_in_picture)
g_socialnetwork=MG_to_G(mg_socialnetwork)

#Degree
nd=NodeDegree(g_socialnetwork)    

#PageRank
np=NodePageRank(g_socialnetwork)

#EdgeRank
er=EdgeRank(g_socialnetwork)



#Belows are for reference only. Not implemented
"""
**Checkpoint**
typecheck.returns("100 * (string, count)")
Top 100 .describe()
"count": 100.0
"mean": 109.96
"std": 52.4777817343
"min": 71.0
"25%": 79.75
"50%": 91.0
"75%": 120.25
"max": 373.0
"""
def degree():
    return [('Alec Baldwin', 82)] * 100

"""
**Checkpoint**
typecheck.returns("100 * (string, number)")
Top 100 .describe()
"count": 100.0
"mean": 0.0001841088
"std": 0.0000758068
"min": 0.0001238355
"25%": 0.0001415028
"50%": 0.0001616183
"75%": 0.0001972663
"max": 0.0006085816
"""
def pagerank():
    return [('Martha Stewart', 0.00019312108706213307)] * 100

"""
**Checkpoint**
typecheck.returns("100 * ((string, string), count)")
Top 100 .describe()
"count": 100.0
"mean": 25.84
"std": 16.0395470855
"min": 14.0
"25%": 16.0
"50%": 19.0
"75%": 29.25
"max": 109.0
"""
def best_friends():
    return [(('Michael Kennedy', 'Eleanora Kennedy'), 41)] * 100
