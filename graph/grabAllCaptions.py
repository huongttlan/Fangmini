############################################
# Grab all raw captions 
# For graph miniproject
###########################################
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import time as tm


########################### iterate over pages #########################
for pg in range(26):
    ### grab all the views and their url, and the event date
    pg_captiondf = pd.DataFrame(columns=('event_url', 'event_date', 'photocaption'))

    if pg == 0:
        pg_url = "http://www.newyorksocialdiary.com/party-pictures"
    else:
        pg_url = "http://www.newyorksocialdiary.com/party-pictures?page=%s" % pg
            
    pg_response = requests.get(pg_url)
    pg_soup = BeautifulSoup(pg_response.text)
    
    print pg_response.url
    
    evt_divs = pg_soup.select('div.views-row')
    print 'number of views on each page: ',len(evt_divs)
    
    
    ####################### iterate over events on each page #################
    t = tm.time()
    pg_captiondf = pd.DataFrame(columns=('event_url', 'event_date', 'photocaption'))
    for evt in range(len(evt_divs)):
        print '-------'
        print 'Event number:' , evt
        evt_captiondf = pd.DataFrame(columns=('event_url', 'event_date', 'photocaption'))
        #print views_divs[k].prettify()
        evt_date = evt_divs[evt].select('span.views-field.views-field-created span.field-content')[0]
        dateword = evt_date.text.split()
        evt_date = datetime.strptime(dateword[1]+'/'+dateword[2][0:-1:1]+'/'+dateword[3], "%B/%d/%Y")
        evt_url = "http://www.newyorksocialdiary.com" + evt_divs[evt].find('a')['href']
        print 'Creation date: ', evt_date
        print 'view_url: ', evt_url
     
        # grab all the captions form each page
        evt_response = requests.get(evt_url)
        evt_soup = BeautifulSoup(evt_response.text)
        captions = evt_soup.select('div.photocaption')
        print 'Caption number: ',len(captions)
        ################### iterate over all the captions, insert item into dateframe ############
        for cp in range(len(captions)):
            caption = captions[cp].text
            evt_captiondf.loc[cp] = [evt_url, evt_date, caption]
            
        print 'Length of event dataframe:', len(evt_captiondf)
        pg_captiondf = pg_captiondf.append(evt_captiondf, ignore_index=True)
        print 'Length of page dataframe:', len(pg_captiondf)
        
    pg_captiondf.to_pickle('Page' + str(pg))
    print 'Time elapsed:', tm.time()-t


# save data on each page
df2 = pd.read_pickle('Page' + str(pg))
print df2.equals(pg_captiondf)
print 'Page', pg, 'is done!'
