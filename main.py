from SimpleCrawler import SimpleCrawler

def main():
    sc = SimpleCrawler("http://knowledgecenter.unr.edu/")
    
    def print_title(soup):
        print soup.title

    sc.add_action(print_title)

    sc.crawl()



main()
