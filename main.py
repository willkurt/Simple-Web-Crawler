from SimpleCrawler import SimpleCrawler

def main():
    sc = SimpleCrawler("http://knowledgecenter.unr.edu/")
    
    def print_title(current, soup):
        print soup.title
        print current


    sc.add_action(print_title)

    sc.crawl()



main()
