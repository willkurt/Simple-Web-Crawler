"""
the goal of this is to make a simple web crawler
to crawl through pages in a website and on each page
be able to perform a specific action
"""
import urllib2
from BeautifulSoup import BeautifulSoup


class SimpleCrawler:
    
    def __init__(self, site_root):
        #actions that will be added later to be performed when each page is visted
        self.actions = []

        #links we've visted
        self.visited = []

        #links to visit
        self.visit_queue = []

        #this is a stack of where we are to allow for backtracking
        self.current_location = []
        self.current_location.append(site_root)

    
