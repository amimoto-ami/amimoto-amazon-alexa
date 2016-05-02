# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import json


if __name__ == "__main__":
    ## ref: pyquery
    # https://media.readthedocs.org/pdf/pyquery/latest/pyquery.pdf
    data = dict()
    file = open('data/attendees.json', "w")
    dom = pq(url='https://2016.europe.wordcamp.org/attendees/')
    entries = dom.find('ul.tix-attendee-list')
    for x in entries('li'):
        twitter_name = pq(x).find('a.tix-attendee-twitter').text()
        full_name = pq(x).find('div.tix-attendee-name').text()
        if twitter_name != None:
            # have more than 3 characters ?
            if len(twitter_name) > 3:
                data[full_name] = twitter_name
    file.write(json.dumps(data, indent=2))
