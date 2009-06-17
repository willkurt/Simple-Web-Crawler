from SimpleCrawler import SimpleCrawler

def main():
    sc = SimpleCrawler("http://knowledgecenter.unr.edu/",ignore_params=True)
    #sc = SimpleCrawler("http://lib-bling.com/")
   
    dot_file = open("crawler_out.dot",'w')
    dot_file.write("digraph crawlerout{\nnode [shape=point];\n")
    def print_title(current, internal_links, soup):
        print soup.title
        print current
        for each in internal_links:
            dot_file.write("\""+current+"\" -> \""+each+"\";\n")
        


    sc.add_action(print_title)

    sc.crawl()
    dot_file.write("/n}")
    

main()
