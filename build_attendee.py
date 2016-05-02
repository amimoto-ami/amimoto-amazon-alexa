from pyquery import PyQuery as pq


if __name__ == "__main__":
    ## ref: pyquery
    # https://media.readthedocs.org/pdf/pyquery/latest/pyquery.pdf
    dom = pq(url='https://2016.europe.wordcamp.org/attendees/')
    entries = dom.find('ul.tix-attendee-list')
    for x in entries('li'): print(pq(x).find('div.tix-attendee-name').text(),
        pq(x).find('a.tix-attendee-twitter').text())

