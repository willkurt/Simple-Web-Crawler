"""
the goal of this is to make a simple web crawler
to crawl through pages in a website and on each page
be able to perform a specific action
"""
import urllib2
from BeautifulSoup import BeautifulSoup


class SimpleCrawler:
    
    def __init__(self, site_root):

        if(site_root[-1] != '/'):
            site_root = site_root+'/'

        #actions that will be added later to be performed when each page is visted
        #all action must accept a BeautifulSoup object
        self.actions = []

        #links we've visted
        self.visited = []

        #links to visit
        self.visit_queue = []
        self.visit_queue.append(site_root)
        print self.visit_queue
       
        #this will temporarly hold the current location
        self.current_location = site_root

        

    def crawl(self):
        while  not self.done():
            self.current_location = self.next_in_queue()
            self.visited.append(self.current_location)
            page = urllib2.urlopen(self.current_location)
            soup = BeautifulSoup(page)
            self.queue_relative_links()
            for action in self.actions:
                action(soup)
           


    """
    for now actions are assumed to be soup objects
    """
    def add_action(self,action):
        self.actions.append(action)
    
    def done(self):
        if(len(self.visit_queue) == 0):
            return True
        else:
            return False

    def next_in_queue(self):
        next = self.visit_queue[0]
        self.visit_queue = self.visit_queue[1:]
        return next

    def queue_relative_links(self):
        pass
