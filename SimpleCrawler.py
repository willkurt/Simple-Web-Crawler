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
        #all actions will be passed a string of the current url and a beautifulsoup object
        self.actions = []
        self.bad_urls = []
        self.other_errors = []
        #links we've visted
        self.visited = []

        #links to visit
        self.visit_queue = []
        self.visit_queue.append(site_root)
        print self.visit_queue
       
        #this will temporarly hold the current location
        self.current_location = site_root

        

    def crawl(self):
        number_crawled = 0
        while  not self.done():
            self.current_location = self.next_in_queue()
            self.visited.append(self.current_location)
            try:
                page = urllib2.urlopen(self.current_location)
                soup = BeautifulSoup(page)
                self.queue_relative_links(soup)
                for action in self.actions:
                    action(self.current_location, soup)
                number_crawled = number_crawled+1
            except urllib2.HTTPError:
                self.bad_urls.append(self.current_location)
                print self.current_location
        print "Done! Crawled "+str(number_crawled)+" pages"

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

    def queue_relative_links(self, soup):
        current_root = self.make_root(self.current_location)
        testresults = open("testresults.txt",'a')
        testresults.write("*****"+self.current_location+"*******\n")
        for each in soup('a'):
            if (each.has_key('href')) and (not "http" in each['href']) and (not "#" in each['href']):
                page_url = self.join_root_relative_link(current_root,each['href'])
                if not page_url in self.visited:
                    self.visit_queue.append(page_url)
                    testresults.write(page_url+"\n")
        testresults.close()

    def join_root_relative_link(self,root,rel_link):
        if(len(rel_link) >= 1 and rel_link[0] == "/"):
            rel_link = rel_link.replace("/","",1)
        return root+rel_link

    def make_root(self, current_location):
        #makes the proper root from the current location
        root = current_location
        if(not current_location[-1] == "/"):
            parts = current_location.split("/")
            parts.remove(parts[-1])
            root = "/".join(parts)+"/"
        return root
