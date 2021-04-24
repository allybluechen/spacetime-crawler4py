import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from report import Report

r = Report()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    urlList = []
    subdomains = []
    parsed = urlparse(url)
    maxwords = 0
    longestpage = ""
    words = []

    if(200 <= resp.status <= 202 and is_valid(url)):
        #get the raw_response content and parse it into HTML using beautifulsoup
        html = bs(resp.raw_response.content, "html.parser")
        #skip if the url is a forum
        if(html.find("embed", {"type": "application/pdf"})):
            return []
        if(not html.find('embed', attrs={'type': "application/pdf"})):
            # find all links from the html and append it to the urlList list
            for link in html.findAll('a', attrs={'href': re.compile("^(http|https)://")}):
                urlList.append(link.get('href'))
                
        words = tokenize(html.getText())
        if maxwords < len(words):
            maxwords = len(words)
            longestpage = url
    if(400 <= resp.status <= 599 and is_valid(url)):
        pass

    # for report.py
    if "ics.uci.edu" in parsed.netloc: #4   
        if parsed.netloc != "ics.uci.edu" and parsed.netloc != "www.ics.uci.edu":
            r.incrementSubdomainCount(url)
    

    print("max words on one page:", maxwords)
    print("longest page:", longestpage) #2 
    print("50 most common words:", output(wordFreq(words))) #3 
    print("subdomains:", output_alpha(wordFreq(subdomains))) #4 

    return urlList


def is_valid(url):
    wanted = ['ics.uci.edu', 'cs.uci.edu','informatics.uci.edu','stat.uci.edu',
    'today.uci.edu/department/information_computer_sciences']
    try:
        parsed = urlparse(url)
        # print(parsed)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if "pdf" in url:
            return False
        if "publications" in url:
            return False
        if "evoke" in url:
            return False
        for validDomain in wanted:
            # remove fragment
            if(parsed.fragment != ''):
                return False
            if validDomain in url:
                return not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                    + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz|ppsx)$", parsed.path.lower())
        return False
        

    except TypeError:
        print("TypeError for ", parsed)
      raise

# Ally's tokenize, wordfreq, and output functions 
def tokenize(contents):
    tokens = re.findall("[\w']+", contents)
    return tokens

def wordFreq(l):
    freq = []
    for w in l:
        freq.append(l.count(w))
    return list(set(zip(l,freq)))


def output_alpha(freq):
    l = []
    freq.sort()
    for i in freq:
        l.append(str(i[0] + ", " + str(i[1])))
    return l
