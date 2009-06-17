"""
the goal of this is to make a simple web crawler
to crawl through pages in a website and on each page
be able to perform a specific action
"""
import urllib2
import HTMLParser
import httplib
from BeautifulSoup import BeautifulSoup


class SimpleCrawler:
    
    def __init__(self, site_root,header_dict = {'User-Agent':'WillBot'},ignore_params = False):

        if(site_root[-1] != '/'):
            site_root = site_root+'/'
    
        self.site_root = site_root
        self.header = header_dict
        #this will ignore paramters after a '?'
        self.ignore_params = ignore_params
        #actions that will be added later to be performed when each page is visted
        #all actions will be passed a string of the current url and a beautifulsoup object
        self.actions = []
        self.bad_urls = []
        self.parse_errors = []
        self.url_errors = []
        #links we've visted
        self.visited = []

        #links to visit
        self.visit_queue = []
        self.visit_queue.append(site_root)
               
        #this will temporarly hold the current location
        self.current_location = site_root

        

    def crawl(self):
        number_crawled = 0
        while  not self.done():
            self.current_location = self.next_in_queue()
            self.visited.append(self.current_location)
            try:
                page = self.open_with_header(self.current_location)
                soup = BeautifulSoup(page)
                internal_links = self.get_internal_pointing_links(soup)
                self.queue_relative_links(internal_links)
                for action in self.actions:
                    action(self.current_location, internal_links,soup)
                number_crawled = number_crawled+1
            except urllib2.HTTPError:
                self.bad_urls.append(self.current_location)
                print "**bad url**"
                print self.current_location
            except HTMLParser.HTMLParseError:
                self.parse_errors.append(self.current_location)
                print "**parse error**"
                print self.current_location
            except urllib2.URLError:
                self.url_errors.append(self.current_location)
                print "**url error**"
                print self.current_location
            if(number_crawled % 50 == 0):
                print "!!!!!!!!!\n"
                print str(number_crawled)+" crawled so far!"
                print "with: "+str(len(self.visit_queue))+" to go!\n"
                print "and "+str(len(self.bad_urls))+" bad urls, "+str(len(self.parse_errors))+" parse errors"
        print "Done! Crawled "+str(number_crawled)+" pages"
        print "With:\n\t"+str(len(self.bad_urls))+" - badurls\n"
        print "\t"+str(len(self.parse_errors))+" - parse errors\n"
        print "\t"+str(len(self.url_errors))+" - url errors\n"
        
    def open_with_header(self, url):
        data = None
        request = urllib2.Request(url,data,self.header)
        return urllib2.urlopen(request)
        
        

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


    #eventually this will need to be refactored into 'queue_relative...' below
    def get_internal_pointing_links(self,soup):
        internal_links = []
        current_root = self.make_root(self.current_location)
        for each in soup('a'):
            page_url = ""
            if each.has_key('href'):
                if(self.site_root.replace("http://","") in each):
                    page_url = each
                elif(not "http" in each['href']) and (not "#" in each['href']):
                    page_url = self.join_root_relative_link(current_root,each['href'])
                if not page_url == "":
                    internal_links.append(page_url)
        return internal_links
                        

     
    """
    not so much 'relative' as links that point back to the current site
    """
    def queue_relative_links(self, internal_links):
        for link in internal_links:
            if not link  in self.visited:
                self.visit_queue.append(link)
        #let's clean up the queue
        self.visit_queue = list(set(self.visit_queue))
        

    def join_root_relative_link(self,root,rel_link):
        
        #I'm not sure this is the best place to remove params, but I can't think of a better one now
        if self.ignore_params and "?" in rel_link:
            rel_link = rel_link.split("?")[0]
        if "../" in rel_link:
            backtrack = rel_link.count("../")
            parts = root.strip("/").split("/")
            root = "/".join(parts[:len(parts)-backtrack])+"/"
            if(len(self.site_root) > root):
                root = site_root
            rel_link = rel_link.replace("../","")
        elif(len(rel_link)>0 and rel_link[0] == "/"):
            rel_link = rel_link[1:]
            root = self.site_root
        
        return root+rel_link

    def make_root(self, current_location):
        #makes the proper root from the current location
        root = current_location
        if(not current_location[-1] == "/"):
            parts = current_location.split("/")
            parts.remove(parts[-1])
            root = "/".join(parts)+"/"
        return root
