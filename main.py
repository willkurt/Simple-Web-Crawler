from SimpleCrawler import SimpleCrawler

def main():
    sc = SimpleCrawler("http://knowledgecenter.unr.edu/",ignore_params=True)
    #sc = SimpleCrawler("http://lib-bling.com/")
    def print_title(current, soup):
        print soup.title
        print current


    sc.add_action(print_title)

    sc.crawl()



main()
