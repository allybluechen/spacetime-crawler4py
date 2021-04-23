import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs



def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    urlList = []
    parsedUrl = urlparse(url)
    if(200 <= resp.status <= 202 and is_valid(url)):
        #get the raw_response content and parse it into HTML using beautifulsoup
        html = bs(resp.raw_response.content, "html.parser")
        if(not html.find('embed', attrs={'type': "application/pdf"})):
            # find all links from the html and append it to the urlList list
            for link in html.findAll('a', attrs={'href': re.compile("^(http|https)://")}):
                urlList.append(link.get('href'))
    if(400 <= resp.status <= 599 and is_valid(url)):
        pass

    return urlList


def is_valid(url):
    wanted = ['ics.uci.edu', 'cs.uci.edu','informatics.uci.edu','stat.uci.edu',
    'today.uci.edu/department/information_computer_sciences']
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        for validDomain in wanted:
            # remove fragment
            if(parsed.fragment != ''):
                return False
            if()
            if validDomain in url:
                return not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                    + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        return False
        

    except TypeError:
        print("TypeError for ", parsed)
        raise


# Oscars implementation, feel free to change
def tokenize(text_file_path: str):
    tokens = []
    with open(text_file_path, 'r') as file:
        for line in file:
            for word in line.split():
                new_word = ""

                for character in word:
                    if character.isalnum():
                        new_word += character
                    else:
                        if new_word != "":
                            new_word = new_word.lower()
                            tokens.append(new_word)
                            new_word = "";
                if new_word != "":
                    new_word = new_word.lower()
                    tokens.append(new_word)
    file.close()
    return tokens
